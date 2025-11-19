r"""
Best-effort metrics extractor for results saved under:
    <tool_dir>/analyzed_buggy_contracts/<BugType>/<ContractName>/...*.report.txt

Usage:
    py -3 scripts\compute_metrics_from_reports.py --tool-dir "D:\\Doof_Ans\\NT547\\results\\MyWebTool" --dataset "D:\\datasets\\SolidiFI-benchmark"

Notes:
- Heuristic extractor: adapts to BugLog files either inside each contract folder or at the bug-type directory level.
- If your .report.txt format is different (JSON with fields, or custom layout), provide one sample report and one sample BugLog so I can refine extraction.
"""
import argparse, csv, re, os, json
from pathlib import Path
from collections import defaultdict

BUG_CODE_MAP = {
    "Re-entrancy": ["reentrancy", "DAO", "External Call To User-Supplied Address".lower()],
    "Timestamp-Dependency": ["timestamp", "Dependence on predictable environment variable".lower()],
    "Unhandled-Exceptions": ["Unchecked Call Return Value".lower(), "UncheckedException".lower(), "unchecked-send"],
    "TOD": ["Transaction-Ordering Dependency".lower(), "TODAmount".lower()],
    "Overflow-Underflow": ["Integer Overflow".lower(), "Integer Underflow".lower(), "Unsigned integer overflow".lower()],
    "Unchecked-Send": ["Unprotected Ether Withdrawal".lower(), "unchecked-send"],
    "tx.origin": ["Use of tx.origin".lower(), "tx-origin"],
}

NUM_RE = re.compile(r'\bsol[:#]?\s*([0-9]+)\b|\bline[:\s]*([0-9]+)\b|(\b[0-9]{1,6}\b)')

def read_buglog_entries(buglog_path: Path):
    # support buglog_path being file or directory containing csv
    if not buglog_path.exists():
        return []
    # if folder, try find first csv inside
    if buglog_path.is_dir():
        candidates = list(buglog_path.glob("*.csv"))
        if not candidates:
            return []
        buglog_path = candidates[0]
    try:
        with buglog_path.open(newline='', encoding='utf-8', errors='ignore') as f:
            rows = list(csv.reader(f))
    except Exception:
        return []
    res = []
    for r in rows[1:]:
        if not r: continue
        try:
            start = int(r[0])
            length = int(r[1]) if len(r) > 1 and r[1].isdigit() else 1
            res.append((start, length))
        except Exception:
            continue
    return res

def try_find_dataset_buglog(dataset_root: Path, bug_type: str, idx: str):
    if not dataset_root:
        return None
    candidates = []
    # common location
    p = Path(dataset_root) / 'buggy_contracts' / bug_type
    if p.exists() and p.is_dir():
        # look for exact name
        cand = p / f'BugLog_{idx}.csv'
        if cand.exists():
            return cand
        # fallback: any file containing idx
        for f in p.glob('BugLog_*.csv'):
            if idx in f.name:
                return f
    return None

def find_report_texts(contract_dir: Path):
    texts = []
    if not contract_dir.exists():
        return texts
    for p in contract_dir.rglob("*.report.txt"):
        try:
            texts.append((p, p.read_text(encoding='utf-8', errors='ignore')))
        except Exception:
            try:
                texts.append((p, p.read_text(encoding='latin-1', errors='ignore')))
            except Exception:
                continue
    return texts

def extract_report_lines_and_tags(text):
    lines = set()
    tags = set()
    # Try parse JSON-report format first
    try:
        data = json.loads(text)
        if isinstance(data, dict) and 'vulnerabilities' in data:
            for v in data.get('vulnerabilities') or []:
                # collect line numbers if present
                ln = v.get('line')
                if isinstance(ln, int):
                    if 0 < ln <= 100000:
                        lines.add(ln)
                else:
                    # try extract numeric from description
                    desc = v.get('description','')
                    for m in NUM_RE.finditer(str(desc)):
                        for g in m.groups():
                            if g:
                                try:
                                    n = int(g)
                                    if 0 < n <= 100000:
                                        lines.add(n)
                                except:
                                    pass
                # collect type/severity as tag
                t = v.get('type') or v.get('severity')
                if t:
                    tags.add(str(t))
            return sorted(lines), tags
    except Exception:
        pass

    # fallback: plain text parsing
    for m in NUM_RE.finditer(text):
        for g in m.groups():
            if g:
                try:
                    n = int(g)
                    # ignore implausible line numbers (>100000)
                    if 0 < n <= 100000:
                        lines.add(n)
                except:
                    pass
    low = text.lower()
    for bug, codes in BUG_CODE_MAP.items():
        for c in codes:
            if c.lower() in low:
                tags.add(bug)
    return sorted(lines), tags

def compute_for_tool(tool_dir: Path, dataset_root: Path, debug: bool=False):
    analyzed = tool_dir / "analyzed_buggy_contracts"
    if not analyzed.exists():
        raise SystemExit(f"No analyzed_buggy_contracts under {tool_dir}")
    per_type = {}
    total_tp = total_fp = total_fn = 0
    mapping_logs = []
    for bug_type_dir in sorted([p for p in analyzed.iterdir() if p.is_dir()], key=lambda x: x.name):
        bug_type = bug_type_dir.name
        injected_count = 0
        tp = fp = fn = 0

        # collect BugLog files at bug_type level for mapping
        buglogs_at_type = {p.name: p for p in bug_type_dir.glob("BugLog_*.csv")} 
        # also include any csv files at that level
        for p in bug_type_dir.glob("*.csv"):
            buglogs_at_type[p.name] = p

        # iterate contract directories (buggy_*.sol folders)
        contracts = [p for p in bug_type_dir.iterdir() if p.is_dir()]
        # also handle case where BugLog files exist but contract folder names differ:
        # we will iterate both: contracts and standalone buglog entries
        seen_buglog_names = set()

        for contract in sorted(contracts, key=lambda x: x.name):
            # try find buglog inside contract first
            candidates = list(contract.rglob("BugLog_*.csv")) + list(contract.rglob("*.csv"))
            buglog = candidates[0] if candidates else None
            matched_csv_path = None

            # fallback: try find BugLog at bug_type level matching contract name number
            if buglog is None:
                # heuristics: if contract is "buggy_12.sol" match "BugLog_12.csv" or "BugLog_12.csv.report" etc
                name = contract.name
                # extract number from contract name
                m = re.search(r'(\d+)', name)
                if m:
                    idx = m.group(1)
                    for candidate_name, pth in buglogs_at_type.items():
                        if idx in candidate_name:
                            # case 1: directory named like the csv containing report file
                            possible_report_in_subdir = pth / (pth.name + ".report.txt")
                            if possible_report_in_subdir.exists():
                                buglog = possible_report_in_subdir
                                # CSV resides inside that dir as pth.name
                                matched_csv_path = pth / pth.name if pth.is_dir() else pth
                                break
                            # case 2: report next to csv e.g. BugLog_1.csv.report.txt
                            possible_report_next = pth.with_name(pth.name + ".report.txt")
                            if possible_report_next.exists():
                                buglog = possible_report_next
                                matched_csv_path = pth
                                break
                            # case 3: csv file exists directly
                            if pth.exists():
                                buglog = pth
                                matched_csv_path = pth
                                break
                    # additional fallback: search any report file under bug_type_dir with idx
                    if buglog is None:
                        for p in bug_type_dir.rglob("*.report.txt"):
                            if idx in p.name or idx in str(p):
                                buglog = p
                                # try deduce csv sibling or parent
                                if p.name.endswith('.report.txt'):
                                    csv_name = p.name.replace('.report.txt','')
                                    csv_candidate = p.with_name(csv_name)
                                    if csv_candidate.exists():
                                        matched_csv_path = csv_candidate
                                if matched_csv_path is None:
                                    # maybe report sits in folder named BugLog_1.csv
                                    parent = p.parent
                                    csv_candidate = parent / (parent.name if parent.name.endswith('.csv') else parent.name + '.csv')
                                    if csv_candidate.exists():
                                        matched_csv_path = csv_candidate
                                break

            if buglog is None:
                # no buglog found for this contract, continue but still check reports (could be FP)
                injected = []
                mapping_logs.append((str(contract), None))
            else:
                # if we detected a matched csv path separately, prefer it for reading injected entries
                csv_for_read = None
                if matched_csv_path:
                    csv_for_read = Path(matched_csv_path)
                else:
                    p = Path(buglog)
                    # if buglog points to a report.txt, try to find sibling csv
                    if p.name.endswith('.report.txt'):
                        csv_name = p.name.replace('.report.txt','')
                        csv_candidate = p.with_name(csv_name)
                        if csv_candidate.exists():
                            csv_for_read = csv_candidate
                        else:
                            # maybe report is inside a folder named like the csv
                            parent = p.parent
                            csv_candidate = parent / (p.name.replace('.report.txt',''))
                            if csv_candidate.exists():
                                csv_for_read = csv_candidate
                    else:
                        csv_for_read = p

                if csv_for_read and csv_for_read.exists():
                    injected = read_buglog_entries(csv_for_read)
                    seen_buglog_names.add(csv_for_read.name)
                    mapping_logs.append((str(contract), str(csv_for_read)))
                else:
                    # try to find CSV in the original dataset if provided
                    idx = None
                    m2 = re.search(r'(\d+)', contract.name)
                    if m2:
                        idx = m2.group(1)
                    dataset_csv = None
                    if dataset_root and idx:
                        dataset_csv = try_find_dataset_buglog(dataset_root, bug_type, idx)
                    if dataset_csv is not None:
                        injected = read_buglog_entries(dataset_csv)
                        seen_buglog_names.add(dataset_csv.name)
                        mapping_logs.append((str(contract), str(dataset_csv)))
                    else:
                        # if no csv found, attempt to read buglog directly (may return empty)
                        injected = read_buglog_entries(Path(buglog) if buglog else Path())
                        if buglog:
                            seen_buglog_names.add(Path(buglog).name)
                            mapping_logs.append((str(contract), str(buglog)))
                

            injected_count += len(injected)
            reports = find_report_texts(contract)
            reported_positions = []
            reported_tags = set()
            for (p, txt) in reports:
                lines, tags = extract_report_lines_and_tags(txt)
                reported_positions.extend(lines)
                reported_tags |= tags

            # decide detection per injected bug entry
            detected_idx = [False]*len(injected)
            for i,(start,length) in enumerate(injected):
                for rl in reported_positions:
                    if start <= rl < start + length:
                        detected_idx[i] = True
                        break
                if not detected_idx[i] and bug_type in reported_tags:
                    detected_idx[i] = True
            tp += sum(1 for v in detected_idx if v)
            fn += sum(1 for v in detected_idx if not v)
            # false positives: reported positions/tags that do not map to any injected interval
            for rl in reported_positions:
                matched = False
                for (start,length) in injected:
                    if start <= rl < start + length:
                        matched = True; break
                if not matched:
                    fp += 1
            if reported_tags and not injected:
                fp += len(reported_tags)

        # handle BugLog files at bug_type level that were not matched to a contract folder
        for bl_name, bl_path in buglogs_at_type.items():
            if bl_name in seen_buglog_names:
                continue
            injected = read_buglog_entries(bl_path)
            if not injected:
                # try to find in dataset by index
                m3 = re.search(r'(\d+)', bl_name)
                if m3 and dataset_root:
                    dataset_csv = try_find_dataset_buglog(dataset_root, bug_type, m3.group(1))
                    if dataset_csv:
                        injected = read_buglog_entries(dataset_csv)
                        seen_buglog_names.add(dataset_csv.name)
                        mapping_logs.append((str(bl_path), str(dataset_csv)))
                    else:
                        continue
                else:
                    continue
            injected_count += len(injected)
            # try find a contract folder matching index
            m = re.search(r'(\d+)', bl_name)
            contract_folder = None
            if m:
                idx = m.group(1)
                candidate = bug_type_dir / f"buggy_{idx}.sol"
                if candidate.exists() and candidate.is_dir():
                    contract_folder = candidate
            reported_positions = []
            reported_tags = set()
            if contract_folder:
                reports = find_report_texts(contract_folder)
                for (p, txt) in reports:
                    lines, tags = extract_report_lines_and_tags(txt)
                    reported_positions.extend(lines)
                    reported_tags |= tags
            # log unmatched buglog at type level
            mapping_logs.append((str(bl_path), str(contract_folder) if contract_folder else None))
            # decide detection as before
            detected_idx = [False]*len(injected)
            for i,(start,length) in enumerate(injected):
                for rl in reported_positions:
                    if start <= rl < start + length:
                        detected_idx[i] = True
                        break
                if not detected_idx[i] and bug_type in reported_tags:
                    detected_idx[i] = True
            tp += sum(1 for v in detected_idx if v)
            fn += sum(1 for v in detected_idx if not v)
            for rl in reported_positions:
                matched = False
                for (start,length) in injected:
                    if start <= rl < start + length:
                        matched = True; break
                if not matched:
                    fp += 1
            if reported_tags and not injected:
                fp += len(reported_tags)

        per_type[bug_type] = {"injected": injected_count, "TP": tp, "FP": fp, "FN": fn}
        total_tp += tp; total_fp += fp; total_fn += fn

    # avg time
    meta = tool_dir / "run_metadata.csv"
    avg_time = None
    samples = 0
    if meta.exists():
        times = []
        try:
            with meta.open(encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for r in reader:
                    try:
                        times.append(float(r.get("time_sec", r.get("time", 0))))
                    except:
                        pass
            if times:
                avg_time = sum(times)/len(times); samples = len(times)
        except Exception:
            pass
    return per_type, total_tp, total_fp, total_fn, avg_time, samples

def safe_div(a,b):
    return a/b if b else float('nan')

def print_summary(tool_name, per_type, tp, fp, fn, avg_time, samples):
    precision = safe_div(tp, tp+fp)
    recall = safe_div(tp, tp+fn)
    f1 = (2*precision*recall/(precision+recall)) if (precision+recall)>0 else float('nan')
    print(f"Tool: {tool_name}")
    print(f"Total TP={tp}, FP={fp}, FN={fn}")
    print(f"Precision: {precision:.3f}, Recall: {recall:.3f}, F1: {f1:.3f}")
    if avg_time is not None:
        print(f"Avg time/contract: {avg_time:.3f}s (n={samples})")
    print("\nPer-bug-type breakdown:")
    print("BugType\tInjected\tTP\tFP\tFN\tPrecision\tRecall\tF1")
    for k,v in per_type.items():
        p = safe_div(v['TP'], v['TP']+v['FP'])
        r = safe_div(v['TP'], v['TP']+v['FN'])
        f = (2*p*r/(p+r)) if (p+r)>0 else float('nan')
        print(f"{k}\t{v['injected']}\t{v['TP']}\t{v['FP']}\t{v['FN']}\t{p:.3f}\t{r:.3f}\t{f:.3f}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tool-dir", required=True, help="Path to results/<ToolName> (contains analyzed_buggy_contracts and run_metadata.csv)")
    parser.add_argument("--dataset", default=None, help="Path to dataset root (not required)")
    parser.add_argument("--debug", action="store_true", help="Print debug mapping of contracts -> buglog files")
    args = parser.parse_args()
    tool_dir = Path(args.tool_dir)
    per_type, tp, fp, fn, avg_time, samples = compute_for_tool(tool_dir, Path(args.dataset) if args.dataset else None, debug=args.debug)
    print_summary(tool_dir.name, per_type, tp, fp, fn, avg_time, samples)
    if args.debug:
        print('\nMapping log (contract_or_buglog -> matched_csv or report):')
        # attempt to print mapping_logs if it exists in compute_for_tool scope via re-computation
        # Recompute small mapping for printing convenience (cheap):
        analyzed = tool_dir / "analyzed_buggy_contracts"
        for bug_type_dir in sorted([p for p in analyzed.iterdir() if p.is_dir()], key=lambda x: x.name):
            for p in bug_type_dir.rglob("*.report.txt"):
                print(f"REPORT: {p}")
            for p in bug_type_dir.glob("BugLog_*.csv"):
                print(f"BUGLOG: {p}")
        print('\nNote: to compute TP/FN correctly the script needs the original dataset BugLog CSVs under the dataset root if results only contain reports. Use --dataset to point to the SolidiFI dataset root.')

if __name__ == '__main__':
    main()
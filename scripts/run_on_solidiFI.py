#!/usr/bin/env python3
"""
run_on_solidiFI.py

Script chạy thử để gửi toàn bộ hợp đồng trong dataset SolidiFI-benchmark
tới API backend của project và lưu báo cáo theo cấu trúc:

  results/<ToolName>/analyzed_buggy_contracts/<BugType>/<ContractName>/<ContractName>.report.txt

Sử dụng (ví dụ):
  py -3 scripts\run_on_solidiFI.py --dataset D:\datasets\SolidiFI-benchmark --backend-url http://localhost:5000/api/v1/analyze --tool-name MyWebTool

Tùy chỉnh các tham số nếu backend của bạn dùng key khác cho payload.
"""
import argparse
import json
import sys
import time
from pathlib import Path
import requests


def read_contract_source(contract_path: Path) -> str:
    """Nếu là folder, gộp tất cả .sol thành một string; nếu là file .sol, đọc trực tiếp."""
    if contract_path.is_dir():
        files = sorted(contract_path.rglob("*.sol"))
        if not files:
            return ""
        contents = []
        for p in files:
            try:
                contents.append(p.read_text(encoding="utf-8"))
            except Exception:
                contents.append("")
        return "\n\n".join(contents)
    else:
        try:
            return contract_path.read_text(encoding="utf-8")
        except Exception:
            return ""


def save_report(output_root: Path, tool_name: str, bug_type: str, contract_name: str, report_text: str):
    out_dir = output_root / tool_name / "analyzed_buggy_contracts" / bug_type / contract_name
    out_dir.mkdir(parents=True, exist_ok=True)
    report_file = out_dir / f"{contract_name}.report.txt"
    report_file.write_text(report_text, encoding="utf-8")
    return report_file


def pretty_response_text(r: requests.Response) -> str:
    # Nếu response là JSON, pretty print; ngược lại trả về text thô
    ct = r.headers.get("Content-Type", "")
    if "application/json" in ct or (r.text and r.text.strip().startswith("{")):
        try:
            j = r.json()
            return json.dumps(j, indent=2, ensure_ascii=False)
        except Exception:
            return r.text
    return r.text


def main():
    parser = argparse.ArgumentParser(description="Send SolidiFI buggy contracts to tool backend and save reports")
    parser.add_argument("--dataset", required=True, help="Path to SolidiFI-benchmark (contains buggy_contracts)")
    parser.add_argument("--backend-url", required=True, help="Full URL to your analyze API endpoint")
    parser.add_argument("--tool-name", default="MyTool", help="Name to use under results/<ToolName>")
    parser.add_argument("--output", default=None, help="Output base folder (default: ./results)")
    parser.add_argument("--timeout", type=float, default=120.0, help="Seconds to wait for backend response")
    parser.add_argument("--payload-key", default="code", help="Primary key name for source code in JSON payload (default: code)")
    parser.add_argument("--concurrency", type=int, default=1, help="Not implemented: placeholder for future parallelism")
    args = parser.parse_args()

    dataset_path = Path(args.dataset)
    buggy_dir = dataset_path / "buggy_contracts"
    if args.output:
        output_root = Path(args.output)
    else:
        output_root = Path.cwd() / "results"

    if not buggy_dir.exists():
        print(f"ERROR: Không tìm thấy folder buggy_contracts trong dataset: {buggy_dir}")
        sys.exit(1)

    summary = []
    headers = {"Content-Type": "application/json"}

    for bug_type_dir in sorted([p for p in buggy_dir.iterdir() if p.is_dir()], key=lambda x: x.name):
        bug_type = bug_type_dir.name
        for contract_path in sorted(bug_type_dir.iterdir(), key=lambda x: x.name):
            contract_name = contract_path.name
            print(f"Processing: {bug_type}/{contract_name}")
            source = read_contract_source(contract_path)
            if not source.strip():
                print("  Skip (no .sol files or empty)")
                continue

            # build payload: include both common keys but allow overriding primary code key
            payload = {args.payload_key: source, "contractName": contract_name, "meta": {"bug_type_folder": bug_type}}
            # Also include 'code' as alternative
            if args.payload_key != "code":
                payload.setdefault("code", source)

            t0 = time.time()
            try:
                r = requests.post(args.backend_url, headers=headers, data=json.dumps(payload), timeout=args.timeout)
                elapsed = time.time() - t0
                if r.status_code == 200:
                    report_text = pretty_response_text(r)
                else:
                    report_text = f"ERROR HTTP {r.status_code}\n{r.text}"
            except Exception as e:
                elapsed = time.time() - t0
                report_text = f"EXCEPTION: {e}"

            saved = save_report(output_root, args.tool_name, bug_type, contract_name, report_text)
            print(f"  Saved report -> {saved} (t={elapsed:.2f}s)")
            summary.append((bug_type, contract_name, elapsed, str(saved)))

    # write metadata CSV next to output root/tool
    meta_dir = output_root / args.tool_name
    meta_dir.mkdir(parents=True, exist_ok=True)
    meta_file = meta_dir / "run_metadata.csv"
    with meta_file.open("w", encoding="utf-8") as f:
        f.write("bug_type,contract_name,time_sec,report_path\n")
        for b, c, t, p in summary:
            f.write(f"{b},{c},{t:.3f},{p}\n")

    print(f"\nDone. Reports saved under: {output_root / args.tool_name}")
    print(f"Metadata: {meta_file}")


if __name__ == "__main__":
    main()

# NT547 - Smart Contract CFG Visualizer

D02: Công cụ Trực quan hóa Đồ thị Luồng Điều khiển (CFG) cho Hợp đồng Thông minh

## Giới thiệu / Introduction

Đây là một công cụ phân tích tĩnh và trực quan hóa Đồ thị Luồng Điều khiển (Control Flow Graph - CFG) cho các hợp đồng thông minh Solidity. Công cụ giúp phân tích cấu trúc luồng điều khiển của các hàm trong smart contract và tạo ra các sơ đồ trực quan dễ hiểu.

This is a static analysis and visualization tool for Control Flow Graphs (CFG) of Solidity smart contracts. The tool helps analyze the control flow structure of functions in smart contracts and generates easy-to-understand visual diagrams.

## Tính năng / Features

- ✅ **Phân tích Tĩnh**: Phân tích mã nguồn Solidity để trích xuất cấu trúc hợp đồng và các hàm
- ✅ **Xây dựng CFG**: Tự động xây dựng đồ thị luồng điều khiển cho mỗi hàm
- ✅ **Trực quan hóa**: Tạo sơ đồ CFG với graphviz (hỗ trợ PNG, PDF, SVG)
- ✅ **CLI Interface**: Giao diện dòng lệnh dễ sử dụng
- ✅ **Hỗ trợ nhiều cấu trúc**: if/else, loops (for, while), return statements, assertions

## Cài đặt / Installation

### Yêu cầu / Requirements

- Python 3.8 trở lên / Python 3.8 or higher
- Graphviz (cần cài đặt trên hệ thống / needs to be installed on system)

### Cài đặt Graphviz / Installing Graphviz

**Ubuntu/Debian:**
```bash
sudo apt-get install graphviz
```

**macOS:**
```bash
brew install graphviz
```

**Windows:**
Download from https://graphviz.org/download/

### Cài đặt công cụ / Installing the tool

```bash
# Clone repository
git clone https://github.com/Whats-up-pro/NT547.git
cd NT547

# Cài đặt dependencies
pip install -r requirements.txt

# Cài đặt package
pip install -e .
```

## Sử dụng / Usage

### Dòng lệnh cơ bản / Basic Command Line

```bash
# Phân tích một file smart contract
cfg-visualizer examples/SimpleToken.sol

# Chỉ định thư mục output và format
cfg-visualizer examples/SimpleToken.sol -o output/mytoken -f pdf

# Phân tích một hàm cụ thể
cfg-visualizer examples/SimpleToken.sol --function transfer

# Tạo visualization kết hợp cho tất cả các hàm
cfg-visualizer examples/Voting.sol --combined

# Verbose output
cfg-visualizer examples/Auction.sol -v
```

### Sử dụng trong Python / Using in Python

```python
from cfg_visualizer import SolidityParser, CFGAnalyzer, CFGVisualizer

# Đọc source code
with open('contract.sol', 'r') as f:
    source_code = f.read()

# Parse contract
parser = SolidityParser(source_code)
parsed_data = parser.parse()

# Phân tích CFG cho mỗi hàm
analyzer = CFGAnalyzer()
cfg_data = analyzer.analyze_function(
    parsed_data['functions'][0]['body'],
    parsed_data['functions'][0]['name']
)

# Tạo visualization
visualizer = CFGVisualizer()
visualizer.visualize(cfg_data, 'output/cfg', format='png')
```

## Cấu trúc Project / Project Structure

```
NT547/
├── src/
│   └── cfg_visualizer/
│       ├── __init__.py          # Package initialization
│       ├── parser.py            # Solidity parser
│       ├── analyzer.py          # CFG analyzer
│       ├── visualizer.py        # CFG visualizer
│       └── cli.py              # Command line interface
├── examples/
│   ├── SimpleToken.sol         # Example: Simple token contract
│   ├── Voting.sol              # Example: Voting contract
│   └── Auction.sol             # Example: Auction contract
├── tests/                      # Unit tests
├── output/                     # Generated visualizations
├── requirements.txt            # Python dependencies
├── setup.py                   # Package setup
└── README.md                  # Documentation
```

## Ví dụ / Examples

### Simple Token Contract

```bash
cfg-visualizer examples/SimpleToken.sol -o output/simple_token
```

Tạo ra CFG cho các hàm:
- `transfer`: Chuyển token với kiểm tra điều kiện
- `mint`: Tạo token mới
- `getBalance`: Truy vấn số dư

### Voting Contract

```bash
cfg-visualizer examples/Voting.sol --combined -o output/voting
```

Phân tích các hàm bỏ phiếu với vòng lặp và điều kiện phức tạp.

### Auction Contract

```bash
cfg-visualizer examples/Auction.sol -v
```

Phân tích hợp đồng đấu giá với logic phức tạp.

## Kiến trúc / Architecture

### 1. Parser Module (`parser.py`)
- Phân tích cú pháp Solidity
- Trích xuất contracts và functions
- Tạo cấu trúc dữ liệu cho analyzer

### 2. Analyzer Module (`analyzer.py`)
- Xây dựng CFG nodes và edges
- Xử lý các cấu trúc điều khiển (if, loops, returns)
- Sử dụng NetworkX để quản lý graph

### 3. Visualizer Module (`visualizer.py`)
- Tạo visualization với Graphviz
- Hỗ trợ nhiều format (PNG, PDF, SVG)
- Tùy chỉnh màu sắc và style cho các loại node

### 4. CLI Module (`cli.py`)
- Giao diện dòng lệnh
- Xử lý arguments và options
- Orchestrate toàn bộ pipeline

## Phát triển / Development

### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest tests/ --cov=cfg_visualizer
```

### Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License

## Tác giả / Authors

NT547 Team

## Tài liệu tham khảo / References

- Solidity Documentation: https://docs.soliditylang.org/
- Graphviz: https://graphviz.org/
- NetworkX: https://networkx.org/
- Control Flow Analysis: https://en.wikipedia.org/wiki/Control-flow_graph

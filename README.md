# NT547 - Solidity CFG Visualizer

## Công cụ Trực quan hóa Đồ thị Luồng Điều khiển (CFG) cho Hợp đồng Thông minh

A web-based tool for visualizing Control Flow Graphs (CFG) of Solidity smart contracts. This tool helps security analysts and developers understand the execution logic of smart contracts by visualizing code structure as interactive graphs.

## 🎯 Tính năng chính (Core Features)

### 1. Giao diện Nhập liệu (Input Interface)
- ✅ **Monaco Editor** - Trình soạn thảo code với syntax highlighting cho Solidity
- ✅ **Themes** - Giao diện tối (dark theme) dễ nhìn
- ✅ **Line numbers** - Hiển thị số dòng để dễ theo dõi
- ✅ **Auto-completion** - Hỗ trợ tự động hoàn thiện code

### 2. Phân tích Cú pháp (Parsing)
- ✅ **@solidity-parser/parser** - Parser Solidity chính thức
- ✅ **AST Generation** - Chuyển đổi code thành Abstract Syntax Tree
- ✅ **Error handling** - Xử lý lỗi cú pháp và hiển thị thông báo rõ ràng
- ✅ **Performance metrics** - Hiển thị thời gian parse

### 3. Xây dựng CFG (CFG Construction)
- ✅ **Basic blocks** - Tạo các khối cơ bản (basic blocks)
- ✅ **Control flow** - Xác định luồng điều khiển
- ✅ **Branch detection** - Phát hiện if/else, switch
- ✅ **Loop detection** - Phát hiện for, while, do-while
- ✅ **Special statements** - Xử lý require, assert, revert
- ✅ **Return statements** - Xử lý lệnh return

### 4. Trực quan hóa (Visualization)
- ✅ **React Flow** - Thư viện visualization đồ thị mạnh mẽ
- ✅ **Interactive nodes** - Các nút có thể click và tương tác
- ✅ **Color-coded** - Màu sắc khác nhau cho các loại khối
- ✅ **Edge labels** - Nhãn trên các cạnh (true/false/loop)
- ✅ **Minimap** - Bản đồ thu nhỏ để quan sát tổng thể
- ✅ **Zoom & Pan** - Phóng to, thu nhỏ và di chuyển đồ thị
- ✅ **Auto-layout** - Tự động sắp xếp vị trí các nút

### 5. Tính Tương tác (Interactivity)
- ✅ **Click to highlight** - Click vào nút để highlight code tương ứng
- ✅ **Multi-function support** - Chọn function để xem CFG
- ✅ **Real-time stats** - Hiển thị số lượng blocks và edges
- ✅ **Line highlighting** - Highlight các dòng code trong editor

## 🚀 Cài đặt (Installation)

### Prerequisites
- Node.js (v16 or higher)
- npm hoặc yarn

### Steps

1. **Clone repository**
```bash
git clone https://github.com/Whats-up-pro/NT547.git
cd NT547
```

2. **Cài đặt dependencies**
```bash
npm install
```

3. **Chạy development server**
```bash
npm run dev
```

4. **Mở trình duyệt**
```
http://localhost:3000
```

## 🏗️ Build cho Production

```bash
npm run build
```

Kết quả build sẽ được tạo trong thư mục `dist/`

Để xem preview của production build:
```bash
npm run preview
```

## 📖 Cách sử dụng (Usage)

1. **Nhập code Solidity** vào editor bên trái
2. **Click nút "Parse & Generate CFG"** để tạo đồ thị
3. **Chọn function** từ dropdown (nếu có nhiều functions)
4. **Xem CFG** ở panel bên phải
5. **Click vào các nút** trong CFG để highlight code tương ứng
6. **Sử dụng controls** để zoom, pan, hoặc fit view

### Ví dụ (Example)

Đoạn code mẫu có sẵn trong editor khi mở app:

```solidity
pragma solidity ^0.8.0;

contract Example {
    uint256 public value;
    
    function setValue(uint256 _value) public {
        require(_value > 0, "Value must be positive");
        
        if (_value > 100) {
            value = 100;
        } else {
            value = _value;
        }
    }
}
```

## 🎨 Giao diện (UI Components)

### Color Scheme

- 🟢 **Entry blocks** - Điểm vào (màu xanh lá)
- 🔴 **Exit blocks** - Điểm ra (màu hồng)
- 🔵 **Condition blocks** - Điều kiện (màu xanh dương)
- 🟣 **Loop blocks** - Vòng lặp (màu tím)
- ⚪ **Normal blocks** - Khối thường (màu trắng)

### Edge Types

- ➡️ **Normal** - Luồng bình thường (đen)
- ✅ **True** - Nhánh đúng (xanh lá)
- ❌ **False** - Nhánh sai (đỏ)
- 🔄 **Loop** - Vòng lặp (tím, đứt nét, có animation)
- ↩️ **Return** - Lệnh return (cam)

## 🛠️ Công nghệ sử dụng (Technologies)

- **React** - UI framework
- **Vite** - Build tool và dev server
- **@solidity-parser/parser** - Parse Solidity code thành AST
- **React Flow** - Visualization library cho đồ thị
- **Monaco Editor** - Code editor (same as VS Code)

## 📚 Documentation

Xem file [DOCUMENTATION.md](./DOCUMENTATION.md) để hiểu chi tiết về:
- AST traversal algorithm
- CFG construction logic
- Implementation details
- Architecture overview

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License.

## 👥 Authors

- NT547 Team

## 🙏 Acknowledgments

- [@solidity-parser/parser](https://github.com/solidity-parser/parser) - Solidity AST parser
- [React Flow](https://reactflow.dev/) - Graph visualization
- [Monaco Editor](https://microsoft.github.io/monaco-editor/) - Code editor

## 📧 Contact

Project Link: [https://github.com/Whats-up-pro/NT547](https://github.com/Whats-up-pro/NT547)

---

Made with ❤️ for the Solidity community
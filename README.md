# NT547 - CFG Visualizer for Solidity Smart Contracts

D02: Công cụ Trực quan hóa Đồ thị Luồng Điều khiển (CFG) cho Hợp đồng Thông minh

---

## 📖 Giới thiệu (Introduction)

Phân tích hợp đồng thông minh Solidity là một công việc phức tạp, đòi hỏi sự hiểu biết sâu về luồng thực thi để đảm bảo tính bảo mật và đúng đắn. Dự án này xây dựng một công cụ web giúp đơn giản hóa quá trình này bằng cách **tự động hóa việc tạo và trực quan hóa Đồ thị Luồng Điều khiển (CFG)**, giúp nhà phát triển dễ dàng gỡ lỗi và kiểm tra logic của hợp đồng.

A web-based tool that allows users to paste Solidity source code and receive an interactive, visual representation of the Control Flow Graph (CFG) for functions in the contract. This is an essential tool for security analysts and developers to understand the execution logic of smart contracts.

---

## ✨ Tóm tắt & Tính năng chính (Abstract & Key Features)

**"CFG Visualizer for Solidity"** là một công cụ web cho phép người dùng dán mã nguồn Solidity và nhận lại ngay lập tức một đồ thị luồng điều khiển tương tác.

### Tính năng nổi bật:

- **Phân tích tự động (Automatic Analysis)**: Chuyển đổi mã nguồn Solidity thành Cây Cú pháp Trừu tượng (AST) và tự động xây dựng CFG cho từng hàm
- **Trực quan hóa tương tác (Interactive Visualization)**: Sử dụng React Flow để hiển thị đồ thị rõ ràng, cho phép người dùng kéo thả, phóng to, thu nhỏ
- **Liên kết mã nguồn và đồ thị (Code-Graph Linking)**: **Tính năng nổi bật nhất** - khi nhấp vào một nút trên đồ thị (ví dụ: một câu lệnh `if`), dòng mã tương ứng trong trình soạn thảo sẽ được tô sáng, giúp theo dõi và gỡ lỗi cực kỳ trực quan
- **Xử lý phía trình duyệt (Browser-Side Processing)**: Toàn bộ quá trình phân tích và trực quan hóa diễn ra trên trình duyệt, đảm bảo tốc độ nhanh và bảo mật mã nguồn cho người dùng

### Core Features:

- **Input Interface**: Simple web interface with a code editor for pasting Solidity source code
- **Syntax Parsing**: Uses @solidity-parser/parser to convert source code to Abstract Syntax Tree (AST)
- **CFG Construction**: Logic to traverse the AST, identify functions, basic blocks, and control flow transfer points
- **Visualization**: Graph visualization using React Flow with interactive features
- **Interactive**: Click on graph nodes to highlight corresponding code lines in the editor

---

## 🏗️ Phương pháp & Kiến trúc (Methodology & Architecture)

Hệ thống hoạt động theo một quy trình 3 bước đơn giản, được thực thi hoàn toàn ở phía Frontend (React):

1. **Phân tích (Parse)**: Mã nguồn Solidity được chuyển thành Cây Cú pháp Trừu tượng (AST) bằng `@solidity-parser/parser`
2. **Xây dựng (Build)**: Một thuật toán duyệt cây AST để xác định các khối lệnh và các điểm rẽ nhánh (if, for, while), từ đó tạo ra các nút (nodes) và cạnh (edges) của CFG
3. **Trực quan hóa (Visualize)**: Dữ liệu CFG được render thành đồ thị tương tác bằng thư viện React Flow

### Kiến trúc hệ thống

The project is structured into two main components:

### Backend (Python Flask)
- **Tối giản (Minimal)**: Chỉ dùng để kiểm tra trạng thái và sẵn sàng cho việc mở rộng trong tương lai
- Simple REST API for health checks
- Extensible for future server-side processing
- CORS enabled for frontend communication

### Frontend (React)
- **Xử lý toàn bộ logic chính (Main Processing Logic)**: Phân tích, xây dựng CFG và trực quan hóa
- Monaco editor for code editing with Solidity syntax highlighting
- @solidity-parser/parser for AST generation
- Custom CFG builder logic
- React Flow for graph visualization
- Interactive node-to-code highlighting

![Giao diện công cụ](https://github.com/user-attachments/assets/a9dc6dce-95be-4822-ae5f-9ce4fa493047)

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** (for backend)
- **Node.js 14+** (for frontend)
- **npm** or **yarn**

> **Windows Users**: See [WINDOWS_SETUP.md](WINDOWS_SETUP.md) for detailed Windows-specific setup instructions.

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Run the backend server:
```bash
python app.py
```

The backend will run on `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The frontend will open at `http://localhost:3000`

## 📁 Project Structure

```
NT547/
├── backend/              # Python Flask backend
│   ├── app.py           # Main Flask application
│   ├── requirements.txt # Python dependencies
│   └── README.md        # Backend documentation
│
├── frontend/            # React frontend
│   ├── public/          # Static files
│   ├── src/
│   │   ├── components/  # React components
│   │   │   ├── CodeEditor.js      # Monaco editor wrapper
│   │   │   └── CFGVisualizer.js   # React Flow visualization
│   │   ├── utils/
│   │   │   └── parser.js          # Solidity parser & CFG builder
│   │   ├── App.js       # Main application
│   │   └── index.js     # Entry point
│   ├── package.json
│   └── README.md        # Frontend documentation
│
└── README.md           # This file
```

## 🎯 Usage

1. **Start both backend and frontend servers** (see Quick Start above)
2. **Open the application** in your browser at `http://localhost:3000`
3. **Enter Solidity code** in the left editor panel (or use the provided sample)
4. **Click "Generate CFG"** to create the control flow graph
5. **Interact with the graph**: 
   - Click nodes to highlight corresponding code
   - Zoom and pan the graph
   - Use the minimap for navigation

## 🔧 Technologies Used

### Frontend
- **React 18**: UI framework
- **@solidity-parser/parser**: Solidity AST parsing
- **React Flow**: Graph visualization
- **Monaco Editor**: Code editor with syntax highlighting
- **Axios**: HTTP client

### Backend
- **Flask**: Python web framework
- **Flask-CORS**: CORS support

## 📊 CFG Features

### Node Types
- **Entry/Exit**: Function boundaries
- **Condition**: If/While/For conditions
- **Branch**: True/False paths
- **Merge**: Convergence points
- **Return**: Return statements
- **Statement**: Regular code blocks

### Supported Constructs
- Function definitions
- If/Else statements
- While loops
- For loops
- Return statements
- Variable declarations
- Expression statements
- Nested control structures

## 🖼️ Screenshots

### Initial Interface
![CFG Visualizer Initial View](https://github.com/user-attachments/assets/af5b4545-45c9-4a2d-a7d6-a5ffb2945c08)

### Control Flow Graph Visualization
![CFG Visualization](https://github.com/user-attachments/assets/a9dc6dce-95be-4822-ae5f-9ce4fa493047)

### Interactive Node Selection
![Interactive Feature](https://github.com/user-attachments/assets/52245b2d-8e4d-4a70-a778-031130d04a94)
*Clicking on nodes highlights corresponding code lines*

---

## 📊 Kết quả đạt được (Results)

Công cụ đã chứng minh khả năng hoạt động hiệu quả với các hợp đồng Solidity có cấu trúc điều khiển đa dạng:

- **Xây dựng CFG chính xác (Accurate CFG Construction)**: Cho các hàm chứa câu lệnh `if-else`, vòng lặp `for`, `while`, và các cấu trúc lồng nhau
- **Tính năng tô sáng hai chiều (Bidirectional Highlighting)**: Hoạt động ổn định, giúp liên kết trực quan giữa logic đồ thị và mã nguồn
- **Hiệu năng tốt (Good Performance)**: Tạo đồ thị gần như ngay lập tức cho các hợp đồng có kích thước vừa và nhỏ
- **Hỗ trợ đa cấu trúc điều khiển (Multiple Control Structures)**: Xử lý thành công các cấu trúc If/Else, While, For và các cấu trúc lồng nhau phức tạp
- **Trực quan hóa tương tác (Interactive Visualization)**: Cho phép người dùng zoom, pan, và tương tác với đồ thị một cách mượt mà

---

## 🔮 Hướng phát triển (Future Work)

1. **Tích hợp phân tích lỗ hổng (Vulnerability Analysis Integration)**: Tự động nhận diện và cảnh báo các mẫu mã có thể chứa lỗ hổng bảo mật (ví dụ: reentrancy) ngay trên đồ thị
2. **Phân tích luồng gọi hàm (Call Graph Analysis)**: Trực quan hóa mối quan hệ gọi hàm giữa các hàm khác nhau trong hợp đồng để cung cấp cái nhìn tổng thể hơn
3. **Hỗ trợ nhiều hợp đồng (Multi-Contract Support)**: Mở rộng khả năng phân tích cho nhiều hợp đồng trong cùng một dự án
4. **Export và Share (Export & Share)**: Cho phép xuất đồ thị dưới dạng hình ảnh hoặc chia sẻ link

---

## 🛠️ Development

### Running Tests
```bash
cd frontend
npm test
```

### Building for Production
```bash
cd frontend
npm run build
```

## 📝 License

MIT

## 👥 Contributors

### UIT - NT547 Course Project

**Nhóm phát triển (Development Team):**

- **Phạm Tấn Gia Quốc** - MSSV: 23521308  
  *Vai trò (Role):* Leader + Main Developer  
  *Trách nhiệm (Responsibilities):* Thiết kế kiến trúc, phát triển core features, code chính

- **Phan Nhựt Thiên** - MSSV: 23521487  
  *Vai trò (Role):* Team Member  
  *Trách nhiệm (Responsibilities):* Hỗ trợ phát triển, testing, documentation

## 🙏 Acknowledgments

- @solidity-parser/parser for Solidity parsing capabilities
- React Flow for excellent graph visualization
- Monaco Editor for the code editing experience
# Chắc chắn không phải là assignment3 ltnc hcmut 242
# Symbol Table Simulation (Functional Programming)

## 📌 Giới thiệu
Đây là bài tập lớn môn **Lập trình nâng cao - CO2039 (HK242)**, mô phỏng **Symbol Table** (bảng ghi đối tượng) trong trình biên dịch bằng ngôn ngữ **Python** và theo phong cách **lập trình hàm** (functional programming). (Symbol Table là một phần nhỏ trong bài tập lớn môn PPL) 

Symbol Table là một cấu trúc dữ liệu quan trọng được trình biên dịch sử dụng trong giai đoạn **phân tích ngữ nghĩa (semantic analysis)**, giúp kiểm tra:
- Biến đã được khai báo hay chưa.
- Gán giá trị có đúng kiểu không.
- Quản lý phạm vi (scope) của biến.

## 🎯 Mục tiêu
Sau khi hoàn thành, chương trình giúp sinh viên:
- Thành thạo các khái niệm **lập trình hàm** (thuần đệ quy).
- Sử dụng **hàm bậc cao** (higher-order functions).
- Vận dụng **danh sách** làm cấu trúc dữ liệu cốt lõi.

## 🛠️ Cấu trúc dự án
Repo gồm các file sau:
.
├── main.py
├── StaticError.py # Log error
├── Symbol.py
├── SymbolTable.py # File cần hiện thực chính
├── TestSuite.py # Chứa ít nhất 50 test case
└── TestUtils.py

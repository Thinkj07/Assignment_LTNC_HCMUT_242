# Symbol Table Simulation (Functional Programming)

## 📌 Giới thiệu
Đây là bài tập lớn môn **Lập trình nâng cao - CO2039 (HK242)**, mô phỏng **Symbol Table** (bảng ghi đối tượng) trong trình biên dịch bằng ngôn ngữ **Python** và theo phong cách **lập trình hàm**.  

Symbol Table là một cấu trúc dữ liệu quan trọng được sử dụng trong giai đoạn **phân tích ngữ nghĩa (semantic analysis)** của trình biên dịch, nhằm:
- Kiểm tra biến đã khai báo hay chưa.
- Đảm bảo gán giá trị đúng kiểu dữ liệu.
- Quản lý phạm vi (scope) của biến trong các block lồng nhau.

---

## 🎯 Mục tiêu
Sinh viên sẽ:
- Thành thạo các khái niệm **lập trình hàm**.
- Sử dụng **hàm bậc cao** (higher-order functions).
- Vận dụng **danh sách** làm cấu trúc dữ liệu cốt lõi.

---

## 🛠️ Cấu trúc dự án
```bash
.
├── main.py
├── Symbol.py
├── SymbolTable.py   # File cần hiện thực chính
├── TestSuite.py     # Chứa ít nhất 50 test case
└── TestUtils.py
```

👉 Chỉ chỉnh sửa **`SymbolTable.py`** và **`TestSuite.py`**.  
👉 Không đổi tên file.

---

## 🚀 Cách chạy chương trình
Clone repo và chạy:
```bash
git clone <repo_url>
cd <repo_name>
```

Chạy chương trình chính:
```bash
python main.py
```

Chạy bộ test:
```bash
python TestSuite.py
```

---

## 📥 Đầu vào
- Mỗi testcase là một danh sách lệnh tương tác với Symbol Table.  
- Các lệnh hợp lệ:

| Lệnh | Mô tả |
|------|-------|
| `INSERT <identifier> <type>` | Thêm biến mới (type: `number` hoặc `string`) |
| `ASSIGN <identifier> <value>` | Gán giá trị cho biến |
| `BEGIN` / `END` | Mở/đóng block (tương tự `{ }` trong C/C++) |
| `LOOKUP <identifier>` | Tìm biến trong bảng |
| `PRINT` | In các biến trong scope hiện tại |
| `RPRINT` | In ngược các biến trong scope hiện tại |

---

## 📤 Đầu ra
- In `success` nếu thao tác hợp lệ.
- In lỗi nếu vi phạm quy tắc.

---

## ❌ Các lỗi ngữ nghĩa
- `Undeclared`: Sử dụng biến chưa khai báo.  
- `Redeclared`: Khai báo lại biến trong cùng phạm vi.  
- `TypeMismatch`: Gán sai kiểu dữ liệu.  
- `UnclosedBlock`: Block chưa được đóng.  
- `UnknownBlock`: Đóng block không tồn tại.  
- `InvalidInstruction`: Lệnh không đúng định dạng.  

---

## 🧩 Ví dụ
### Input
```text
INSERT x number
INSERT y string
BEGIN
  INSERT x number
  LOOKUP x
  LOOKUP y
END
```

### Output
```text
success
success
success
1
0
```

---

## 📑 Quy tắc lập trình
- Không sử dụng vòng lặp (`for`, `while`, ...).  
- Không định nghĩa lớp, biến toàn cục.  
- Mọi biến phải **bất biến** (immutable).  
- Chỉ được import:
  ```python
  from StaticError import *
  from Symbol import *
  from functools import *
  ```

---

## 📝 Yêu cầu nộp
- Nộp **2 file**: `SymbolTable.py` và `TestSuite.py`.  
- `TestSuite.py` phải có **ít nhất 50 test case**.  
- Nộp qua hệ thống, **không chấp nhận bài trễ**.  

---

## ⚖️ Quy định
- Sinh viên **tự làm**, không chia sẻ code.  
- Giảng viên có toàn quyền quyết định kết quả cuối.  
- Không cung cấp test case sau khi chấm, chỉ có hướng dẫn chiến lược test.  

---

✍️ **Tác giả**: ThS. Trần Ngọc Bảo Duy, CN. Thi Khắc Quân  
📅 **Tháng 03/2025 – Đại học Bách Khoa, ĐHQG-HCM**

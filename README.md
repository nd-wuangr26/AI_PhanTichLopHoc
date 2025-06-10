# AI_PhanTichLopHoc

AI_PhanTichLopHoc là một ứng dụng dựa trên Flask, sử dụng các mô hình AI để phân tích hành vi trong lớp học. Ứng dụng xử lý video đầu vào để phân loại các hoạt động như học tập, ngủ, và các hoạt động khác, sau đó lưu kết quả vào cơ sở dữ liệu MySQL. Ngoài ra, ứng dụng cung cấp giao diện web để hiển thị thống kê và biểu đồ.

## Chức năng

- **Phân tích video theo thời gian thực**: 
  - Xử lý từng khung hình từ video để phân loại hành vi (học tập, ngủ, hoạt động khác).
  - Sử dụng mô hình ONNX hoặc PyTorch để dự đoán.

- **Lưu trữ dữ liệu**:
  - Lưu kết quả phân tích vào cơ sở dữ liệu MySQL.
  - Dữ liệu bao gồm số lượng hành vi theo từng loại và thời gian ghi nhận.

- **Hiển thị thống kê**:
  - Giao diện web hiển thị dữ liệu lịch sử dưới dạng bảng.
  - Biểu đồ thống kê theo ngày, tháng, năm.

- **API REST**:
  - `/api/chart-day`: Trả về thống kê theo ngày.
  - `/api/chart-month`: Trả về thống kê theo tháng.
  - `/api/chart-year`: Trả về thống kê theo năm.

- **Tùy chỉnh bộ lọc**:
  - Lọc dữ liệu theo ngày, tháng, năm trên giao diện web.

## Cấu trúc Dự án

```yaml
AI_PhanTichLopHoc/
├── app.py                # Ứng dụng Flask chính sử dụng mô hình PyTorch
├── app_onnx.py           # Ứng dụng Flask sử dụng mô hình ONNX Runtime
├── my_model.py           # Logic tải và dự đoán với mô hình PyTorch
├── my_model_onnx.py      # Logic tải và dự đoán với mô hình ONNX
├── test_connect.py       # Script kiểm tra kết nối MongoDB
├── test_frame.jpg        # Hình ảnh mẫu để kiểm tra mô hình
├── test.mp4              # Video mẫu để kiểm tra mô hình
├── test.py               # Unit tests cho ứng dụng
├── model/
│   ├── best.pt           # Mô hình PyTorch đã huấn luyện
│   └── best.onnx         # Mô hình ONNX đã chuyển đổi
├── static/
│   └── style.css         # File CSS cho giao diện web
├── templates/
│   └── index.html        # Template HTML của giao diện web
└── .idea/                # Cấu hình IDE (PyCharm hoặc tương tự)
```
## Yêu cầu

- Python 3.10
- MySQL
- Các thư viện Python (xem `requirements.txt`):
  - Flask
  - OpenCV
  - MySQL Connector
  - ONNX Runtime (cho mô hình ONNX)
  - Ultralytics (cho mô hình PyTorch)
## Tạo bảng cơ sở dữ liệu (SQL - tùy chọn)

Nếu bạn sử dụng **MySQL** (hoặc một hệ quản trị cơ sở dữ liệu quan hệ khác) để lưu trữ dữ liệu trạng thái sinh viên, hãy tạo bảng theo cú pháp dưới đây:

```sql
CREATE TABLE detections (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME NOT NULL,
    study_count INT NOT NULL,
    sleep_count INT NOT NULL,
    other_count INT NOT NULL
);
```
## Cài đặt

1. Clone repository:
   ```bash
   git clone https://github.com/your-repo/AI_PhanTichLopHoc.git
   cd AI_PhanTichLopHoc

# AI_PhanTichLopHoc

Mô tả:
Dự án “Giám sát lớp học bằng Deep Learning” sử dụng camera kết hợp mô hình YOLOv8 để phát hiện sinh viên và mô hình ResNet-18 để phân loại trạng thái: học tập, ngủ, hoặc làm việc riêng. Kết quả được lưu vào cơ sở dữ liệu MySQL theo thời gian thực với cơ chế ghi đè theo từng mốc thời gian. Giao diện Flask hiển thị video trực tiếp, bảng thống kê và biểu đồ phân tích theo ngày, tháng, năm. Hệ thống giúp giảng viên theo dõi và đánh giá mức độ tập trung của sinh viên một cách trực quan và hiệu quả.

## Mục tiêu dự án

- Xây dựng hệ thống sử dụng camera giám sát lớp học và tự động phân tích hành vi sinh viên.
- Nhận diện khuôn mặt sinh viên, trích xuất từng đối tượng.
- Phân loại trạng thái của từng sinh viên trong thời gian thực.
- Lưu trữ dữ liệu vào cơ sở dữ liệu để phục vụ việc thống kê, báo cáo.

---

## Mô hình AI sử dụng

- **YOLOv8n (Object Detection)**  
  → Phát hiện sinh viên trong khung hình.

- **ResNet18 (Image Classification)**  
  → Phân loại trạng thái từng sinh viên.

>  Mô hình đã được huấn luyện và được lưu trữ trên [Hugging Face](https://huggingface.co/) để tránh giới hạn của GitHub (không chứa file `.pt` trong repo).

---

##  Công nghệ sử dụng

- `Flask` – Web framework để xây dựng API và giao diện
- `OpenCV` – Xử lý ảnh/video thời gian thực
- `Pytorch` – Huấn luyện mô hình phân loại trạng thái
- `MySQL` – Cơ sở dữ liệu lưu trữ thông tin trạng thái theo thời gian
- `Chart.js` – Hiển thị biểu đồ thống kê (ngày/tháng/năm)
- `HTML/CSS/JS` – Giao diện đơn giản cho quản trị

---

##  Giao diện hệ thống

- Trang xem camera trực tiếp
- Thống kê số lượng sinh viên theo trạng thái
- Biểu đồ tổng hợp trạng thái theo thời gian

---

##  Cấu trúc thư mục
```
Flask_ClassMonitor/
│
├── static/ # CSS
├── templates/ # Giao diện HTML
├── model_detection/ # Mô hình YOLOv8 (chuyển sang HuggingFace)
├── model_classification/ # Mô hình ResNet (chuyển sang HuggingFace)
├── utils/ # Các hàm xử lý AI
├── app.py # Flask app
├── requirements.txt
└── README.md
```
##  Cách chạy dự án

### 1. Clone repo

```bash
git clone https://github.com/nd-wuangr26/AI_PhanTichLopHoc.git
cd AI_PhanTichLopHoc
```
### 2. Install thư viện

```
pip install -r requirements.txt
```

### 3. Tải model từ Hugging Face

1. Model detection
```
https://huggingface.co/NDQ26/ClassMonitor_Detection
```

2. Model detection
```
https://huggingface.co/NDQ26/ClassMonitor_Classification
```

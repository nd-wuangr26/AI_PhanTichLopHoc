from ultralytics import YOLO

# Load model một lần khi import
model = YOLO("model/best.pt")  # Đường dẫn tới file .pt của bạn

def load_model_and_predict(frame):
    results = model(frame, verbose=False)
    if not results:
        return []

    names = results[0].names
    class_ids = results[0].boxes.cls.tolist()
    labels = [names[int(cls)] for cls in class_ids]
    return labels  # Trả về danh sách các nhãn

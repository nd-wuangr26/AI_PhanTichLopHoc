import torch
import cv2
from utils.load_resnet18 import load_model
from torchvision import transforms
from ultralytics import YOLO

# --- Cấu hình ---
YOLO_MODEL_PATH = r'..\Flask_ClassMonitor\model_detection\best.pt'
CLASSIFIER_MODEL_PATH = r'..\Flask_ClassMonitor\model_classification\best.pt'
CLASS_NAMES = ['study', 'sleep', 'other']
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# --- Load YOLO ---
yolo_model = YOLO(YOLO_MODEL_PATH)
yolo_model = yolo_model.to(device)
yolo_model.eval()
yolo_imgsz = 640

# --- Load classification model ---
cls_model = load_model(CLASSIFIER_MODEL_PATH, device, num_classes=len(CLASS_NAMES))
cls_model.eval()

# --- Preprocessing classification ---
preprocess_cls = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])

def preprocess_classification(crop):
    img_rgb = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)
    tensor = preprocess_cls(img_rgb)
    return tensor.unsqueeze(0).to(device)

def detect_and_classify(frame):
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = yolo_model(img, imgsz=640)

    boxes = results[0].boxes

    if boxes is None:
        return []

    xyxy = boxes.xyxy.cpu().numpy()
    confs = boxes.conf.cpu().numpy()
    clses = boxes.cls.cpu().numpy()

    results_list = []
    for i in range(len(xyxy)):
        x1, y1, x2, y2 = map(int, xyxy[i])
        conf = confs[i]
        cls = int(clses[i])

        if cls != 0 or conf < 0.3:  # chỉ nhận người
            continue

        person_crop = frame[y1:y2, x1:x2]
        if person_crop.size == 0:
            continue

        cls_input_tensor = preprocess_classification(person_crop)
        with torch.no_grad():
            output = cls_model(cls_input_tensor)
            class_id = int(torch.argmax(output, dim=1).item())

        results_list.append({
            "box": (x1, y1, x2, y2),
            "label": CLASS_NAMES[class_id]
        })

    return results_list
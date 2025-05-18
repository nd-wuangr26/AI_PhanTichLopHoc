import onnxruntime as ort
import numpy as np
import cv2

# Load ONNX model
session = ort.InferenceSession("model/best.onnx")

# Gán kích thước đầu vào cố định (tùy theo model bạn dùng)
input_width = 640
input_height = 640

input_name = session.get_inputs()[0].name

names = ['study', 'sleep', 'other']  # hoặc tùy theo mô hình của bạn

def preprocess(frame):
    img = cv2.resize(frame, (input_width, input_height))
    img = img / 255.0
    img = img.transpose(2, 0, 1)  # HWC → CHW
    img = np.expand_dims(img, axis=0).astype(np.float32)
    return img

def load_model_and_predict(frame):
    input_tensor = preprocess(frame)
    outputs = session.run(None, {input_name: input_tensor})
    detections = outputs[0][0]  # Tùy định dạng ONNX đầu ra của bạn

    labels = []
    for det in detections:
        conf = det[4]
        class_id = int(det[5])
        print(f"class_id: {class_id}, names length: {len(names)}")  # Debug
        if conf > 0.5:
            labels.append(names[class_id])
    return labels

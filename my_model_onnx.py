import onnxruntime as ort
import numpy as np
import cv2

# Load ONNX model
session = ort.InferenceSession("model/best.onnx", providers=["CPUExecutionProvider"])
input_name = session.get_inputs()[0].name

# Danh sách nhãn
CLASS_NAMES = ['study', 'sleep', 'other']
NUM_CLASSES = len(CLASS_NAMES)

def preprocess(frame):
    img = cv2.resize(frame, (640, 640))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img.transpose(2, 0, 1).astype(np.float32) / 255.0
    img = np.expand_dims(img, axis=0)
    return img

def load_model_and_predict(frame):
    input_tensor = preprocess(frame)
    outputs = session.run(None, {input_name: input_tensor})
    predictions = outputs[0][0]  # Shape: (num_boxes, 85)

    results = []

    for pred in predictions:
        conf = pred[4]
        class_scores = pred[5:5+NUM_CLASSES]  # Chỉ lấy đúng số lớp (3)
        class_id = np.argmax(class_scores)
        score = class_scores[class_id]

        if conf * score > 0.5:
            results.append(CLASS_NAMES[class_id])

    return results

import onnxruntime
import numpy as np
import cv2

# Định nghĩa nhãn lớp (theo model của bạn)
names = ['study', 'sleep', 'other']

# Load ONNX model 1 lần
session = onnxruntime.InferenceSession("model/best.onnx", providers=["CPUExecutionProvider"])
input_name = session.get_inputs()[0].name

def preprocess(img):
    img_resized = cv2.resize(img, (640, 640))
    img_rgb = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)
    img_transposed = img_rgb.transpose(2, 0, 1) / 255.0  # [HWC] -> [CHW]
    img_input = np.expand_dims(img_transposed, axis=0).astype(np.float32)
    return img_input, img.shape[:2], img_resized.shape[:2]

def postprocess(output, orig_shape, resized_shape, conf_thres=0.4):
    preds = output[0]  # (1, 7, 8400)
    preds = np.squeeze(preds).T  # (8400, 7)

    boxes = preds[:, :4]
    scores = preds[:, 4]
    class_probs = preds[:, 5:]

    class_ids = np.argmax(class_probs, axis=1)
    confidences = scores * class_probs[np.arange(len(class_probs)), class_ids]

    mask = confidences > conf_thres
    boxes = boxes[mask]
    confidences = confidences[mask]
    class_ids = class_ids[mask]

    # Chuyển box từ [cx, cy, w, h] => [x1, y1, x2, y2]
    boxes_xyxy = np.empty_like(boxes)
    boxes_xyxy[:, 0] = boxes[:, 0] - boxes[:, 2] / 2
    boxes_xyxy[:, 1] = boxes[:, 1] - boxes[:, 3] / 2
    boxes_xyxy[:, 2] = boxes[:, 0] + boxes[:, 2] / 2
    boxes_xyxy[:, 3] = boxes[:, 1] + boxes[:, 3] / 2

    # Scale box về size gốc
    gain = max(resized_shape) / max(orig_shape)
    pad_x = (resized_shape[1] - gain * orig_shape[1]) / 2
    pad_y = (resized_shape[0] - gain * orig_shape[0]) / 2
    boxes_xyxy[:, [0, 2]] -= pad_x
    boxes_xyxy[:, [1, 3]] -= pad_y
    boxes_xyxy /= gain

    return boxes_xyxy, confidences, class_ids

def predict_from_image(image_path):
    img = cv2.imread(image_path)
    img_input, orig_shape, resized_shape = preprocess(img)
    output = session.run(None, {input_name: img_input})
    boxes, scores, class_ids = postprocess(output, orig_shape, resized_shape)

    labels = [names[int(cls)] for cls in class_ids]
    return labels, boxes, class_ids

labels, boxes, class_ids = predict_from_image("test_frame.jpg")
print("Labels:", labels)
print("Boxes:", boxes)
print("Classes:", class_ids)

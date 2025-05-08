from my_model import load_model_and_predict
import cv2
from collections import Counter

frame = cv2.imread("test_frame.jpg")
labels = load_model_and_predict(frame)
print(labels)
counts = Counter(labels)
study_count = counts.get("study", 0)
sleep_count = counts.get("sleep", 0)
other_count = counts.get("other", 0)
print(study_count, sleep_count, other_count)

from test import predict_from_image
labels, boxes, class_ids = predict_from_image("test_frame.jpg")
print("Labels:", labels)
print("Boxes:", boxes)
print("Classes:", class_ids)

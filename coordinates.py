import cv2
import torch

# Load YOLOv8 model
model = torch.hub.load('ultralytics/yolov5', 'custom', path='weights.pt')  # Replace with your model path

# Open webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Perform YOLO detection
    results = model(frame)

    # Get detection results
    for result in results.xyxy[0]:  # Bounding boxes
        x1, y1, x2, y2, conf, cls = result.numpy()
        
        # Compute center of bounding box (2D position)
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2

        # Draw bounding box
        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
        cv2.circle(frame, (int(center_x), int(center_y)), 5, (0, 0, 255), -1)

    cv2.imshow("YOLO Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

import cv2
from ultralytics import YOLO

model = YOLO("yolov8n.pt")  # Load YOLO model
cap = cv2.VideoCapture(0)  # Start webcam

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    results = model(frame)  # Run YOLO
    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Get bounding box
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2  # Compute center
            cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)  # Mark center
            cv2.putText(frame, f"({cx},{cy})", (cx, cy - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    cv2.imshow("YOLO Tracking", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

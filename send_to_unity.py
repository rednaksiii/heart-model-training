from ultralytics import YOLO
import cv2
import socket
import json

# Load YOLOv8 model
model = YOLO('weights.pt')  # Provide full path if needed

# Setup UDP
UDP_IP = "127.0.0.1"
UDP_PORT = 5065
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Webcam
cap = cv2.VideoCapture(1)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)[0]

    for box in results.boxes:
        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2
        depth_z = 50  # placeholder

        data = {
            "x": float(center_x),
            "y": float(center_y),
            "z": float(depth_z),
            "roll": 0.0,
            "pitch": 0.0,
            "yaw": 0.0
        }

        message = json.dumps(data)
        sock.sendto(message.encode(), (UDP_IP, UDP_PORT))

    cv2.imshow("YOLO Tracking", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

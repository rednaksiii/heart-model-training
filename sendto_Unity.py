import cv2
import torch
import socket
import json

# Load YOLO model
model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt')  # Replace with your model

# Set up UDP socket
UDP_IP = "127.0.0.1"  # Localhost (change if needed)
UDP_PORT = 5065        # Port for communication
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Open webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Perform YOLO detection
    results = model(frame)

    for result in results.xyxy[0]:  # Bounding boxes
        x1, y1, x2, y2, conf, cls = result.numpy()

        # Compute center (X, Y) and depth (Z)
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2
        depth_z = 50  # Placeholder (use real depth calculation)

        # Create data dictionary
        data = {
            "x": float(center_x),
            "y": float(center_y),
            "z": float(depth_z),
            "roll": 0.0,  # Placeholder
            "pitch": 0.0,  # Placeholder
            "yaw": 0.0  # Placeholder
        }

        # Send data as JSON
        message = json.dumps(data)
        sock.sendto(message.encode(), (UDP_IP, UDP_PORT))

    cv2.imshow("YOLO Tracking", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

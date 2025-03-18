from ultralytics import YOLO

# Load the trained YOLO model
model = YOLO("weights.pt")

# Export to ONNX format
model.export(format="onnx")

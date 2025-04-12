from ultralytics import YOLO
import argparse

def convert(weights_path, output_path="weights.onnx", img_size=640):
    # Load YOLOv8 model
    model = YOLO(weights_path)

    # Export to ONNX
    model.export(format="onnx", imgsz=img_size, dynamic=True, simplify=True, opset=11, half=False, device="cpu")
    print(f"✅ Exported {weights_path} to ONNX format.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', type=str, default='weights-roboflow3.pt', help='Path to .pt file')
    parser.add_argument('--output', type=str, default='weights.onnx', help='Output ONNX path')  # not used by Ultralytics API but kept for consistency
    args = parser.parse_args()

    convert(args.weights, args.output)

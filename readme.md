# 🚀 YOLO Model Conversion and Testing

This repository contains scripts and model weights for converting and testing YOLO models across different formats, including ONNX and CoreML.

## 📂 Files Overview

- 📄 **pt-to-coreml.py** - Converts PyTorch (`.pt`) model weights to CoreML format for iOS applications. (Has bugs at the moment)
- 📄 **yolo-to-onnx.py** - Converts YOLO PyTorch weights (`.pt`) to ONNX format.
- 🧪 **testing.py** - Script to test the converted models.
- 📦 **weights.pt** - YOLO model weights in PyTorch format.
- 📦 **weights.onnx** - YOLO model weights in ONNX format.
- ⚠️ **.DS_Store** - A macOS system file that can be ignored.

## 🛠️ Usage

### 🔄 Convert PyTorch Model to ONNX
```bash
python yolo-to-onnx.py
```

### 🍏 Convert PyTorch Model to CoreML
```bash
python pt-to-coreml.py
```

### 🧪 Test Model
Modify `testing.py` as needed and run:
```bash
python testing.py
```

## 📌 Requirements

Make sure you have the required dependencies installed:
```bash
pip install torch onnx coremltools
```

## 🔎 Notes

- ✅ Ensure the correct version of YOLO is used in the conversion scripts.
- 🚀 The ONNX model can be further optimized using tools like `onnxruntime` or `onnx-simplifier`.
- 🍏 The CoreML model is meant for Apple devices and can be tested with Xcode's CoreML tools.

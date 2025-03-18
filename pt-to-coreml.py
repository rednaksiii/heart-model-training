import torch
import coremltools as ct
import torch.nn as nn

# ==========================
# 🔹 Step 1: Load Model Correctly
# ==========================
def load_model(weights_path):
    try:
        # Allow Ultralytics models if needed
        from ultralytics.nn.tasks import DetectionModel
        torch.serialization.add_safe_globals([DetectionModel])

        # Load the full model checkpoint
        model = torch.load(weights_path, map_location=torch.device("cpu"), weights_only=False)
        if isinstance(model, dict):  # If state_dict, load manually
            raise ValueError("Detected state_dict, trying manual load...")
        model.eval()
        print("✅ Loaded full model checkpoint.")
        return model
    except Exception as e:
        print(f"⚠️ Full model load failed: {e}\nTrying state_dict...")

    # If full model load fails, assume it's a state_dict
    class YourModel(nn.Module):
        def __init__(self):
            super().__init__()
            self.conv = nn.Conv2d(3, 16, kernel_size=3, stride=1, padding=1)
            self.relu = nn.ReLU()
            self.fc = nn.Linear(16 * 224 * 224, 10)  # Adjust based on your model

        def forward(self, x):
            x = self.conv(x)
            x = self.relu(x)
            x = x.view(x.size(0), -1)
            x = self.fc(x)
            return x

    model = YourModel()
    model.load_state_dict(torch.load(weights_path, map_location=torch.device("cpu"), weights_only=True))
    model.eval()
    print("✅ Loaded model from state_dict.")
    return model

# ==========================
# 🔹 Step 2: Convert to TorchScript
# ==========================
def convert_to_torchscript(model):
    example_input = torch.rand(1, 3, 224, 224)  # Adjust input shape if needed
    traced_model = torch.jit.trace(model, example_input)
    traced_model.save("traced_model.pt")
    print("✅ Model traced and saved as traced_model.pt")
    return traced_model, example_input

# ==========================
# 🔹 Step 3: Convert to Core ML
# ==========================
def convert_to_coreml(traced_model, example_input):
    mlmodel = ct.convert(traced_model, inputs=[ct.TensorType(shape=example_input.shape)])
    mlmodel.save("model.mlpackage")
    print("✅ Converted to Core ML and saved as model.mlpackage")

# ==========================
# 🔥 Run Full Conversion
# ==========================
if __name__ == "__main__":
    weights_path = "weights.pt"  # Change if needed
    model = load_model(weights_path)
    traced_model, example_input = convert_to_torchscript(model)
    convert_to_coreml(traced_model, example_input)

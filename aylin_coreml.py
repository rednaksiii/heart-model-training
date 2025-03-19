import torch
from ultralytics import YOLO

"""def trace_model(model, example_input):
    return torch.jit.trace(model, example_input)

model = YOLO("weights.pt")
traced_model = trace_model(model, torch.rand(1, 3, 224, 224))


import torch

def script_model(model):
    return torch.jit.script(model)

# Example usage
scripted_model = script_model(model)

import coremltools as ct

def convert_to_coreml(torchscript_model, input_shape):
    mlmodel = ct.convert(
        torchscript_model,
        inputs=[ct.TensorType(shape=input_shape)]
    )
    return mlmodel

# Example usage
coreml_model = convert_to_coreml(traced_model, (1, 3, 224, 224))
coreml_model.save("my_model.mlmodel")"""


from ultralytics import YOLO
import coremltools.libcoremlpython as coremlpython
import coremltools.libmilstoragepython as milstoragepython

model=YOLO('weights.pt')

model.export(format='coreml',nms=False)


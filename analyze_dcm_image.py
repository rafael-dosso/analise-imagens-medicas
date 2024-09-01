import torchxrayvision as xrv
import torch, torchvision
import numpy as np

# Prepare the image:
img = xrv.utils.read_xray_dcm('dicom_samples/id_0a1a0de9-947c36de-38f2e3c9-a497807e-7ceb75f8/Study_72682317.56696215.32367375.69516389.09416010/Series_94559003.83259051.98386686.73459116.65935633/image-49456968-50961677-93916823-30114741-97249659.dcm')
# img = xrv.datasets.normalize(img, 1024) # convert 8-bit image to [-1024, 1024] range
img = (img - img.min()) / (img.max() - img.min()) * 2048 - 1024

if len(img.shape) == 2:
    img = img[np.newaxis, ...]

transform = torchvision.transforms.Compose([xrv.datasets.XRayCenterCrop(),xrv.datasets.XRayResizer(224)])

img = transform(img)
img = torch.from_numpy(img)

# Load model and process image
model = xrv.models.DenseNet(weights="densenet121-res224-all")
outputs = model(img[None,...]) # or model.features(img[None,...]) 

# Print results
for key, value in dict(zip(model.pathologies,outputs[0].detach().numpy())).items():
    print(f"{key}: {value}")
import torchxrayvision as xrv
import torch, torchvision
import numpy as np

def get_diagnosis(dicom_image_path: str)->None:
    """
    Utiliza o modelo pré-treinado do torchxrayvision para classificar a probabilidade de
    patologias da imagem DICOM especificada
    Args:
        dicom_image_path (str): Caminho do arquivo da imagem DICOM
    """
    # Prepare the image:
    img = xrv.utils.read_xray_dcm(dicom_image_path)
    # img = xrv.datasets.normalize(img, 1024) # convert 8-bit image to [-1024, 1024] range
    img = (img - img.min()) / (img.max() - img.min()) * 2048 - 1024 # normalizar imagem

    if len(img.shape) == 2:
        img = img[np.newaxis, ...]

    transform = torchvision.transforms.Compose([xrv.datasets.XRayCenterCrop(),xrv.datasets.XRayResizer(224)])

    img = transform(img)
    img = torch.from_numpy(img)

    # Load model and process image
    model = xrv.models.DenseNet(weights="densenet121-res224-all")
    outputs = model(img[None,...]) # or model.features(img[None,...]) 

    # Print results
    return dict(zip(model.pathologies,outputs[0].detach().numpy()))
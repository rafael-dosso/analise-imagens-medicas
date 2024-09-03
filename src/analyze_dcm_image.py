import torchxrayvision as xrv
import torch, torchvision
import numpy as np

def convert_float32_to_float(input_dict):
    """
    Itera sobre um dicionário e converte valores float32 para float.
    Args:
        input_dict (dict): O dicionário a ser iterado.
    Returns:
        dict: O dicionário com valores convertidos para float.
    """
    for key, value in input_dict.items():
        if isinstance(value, np.float32):
            input_dict[key] = float(value)
    return input_dict

def get_diagnosis(dicom_path: str)->None:
    """
    Utiliza o modelo pré-treinado do torchxrayvision para classificar a probabilidade de
    patologias da imagem DICOM especificada
    Args:
        dicom_path (str): Caminho do arquivo da imagem DICOM
    """
    # Prepare the image:
    img = xrv.utils.read_xray_dcm(dicom_path)
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

    result = dict(zip(model.pathologies,outputs[0].detach().numpy()))
    return convert_float32_to_float(result)
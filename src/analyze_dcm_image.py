import torchxrayvision as xrv
import torch, torchvision
import numpy as np
import pydicom
import warnings

def convert_float32_to_float(input_dict: dict[str,int])->None:
    """
    Itera sobre um dicionário e converte valores float32 para float.
    Args:
        input_dict (dict): O dicionário a ser iterado.
    Returns:
        dict: Novo dicionário com valores convertidos para float.
    """
    for key, value in input_dict.items():
        if isinstance(value, np.float32):
            input_dict[key] = float(value)
    return input_dict

def read_xray_dcm(path: str) -> np.ndarray:
    """read a dicom-like file and convert to numpy array 

    Args:
        path (PathLike): path to the dicom file

    Returns:
        ndarray: 2D single array image for a dicom image scaled between -1024, 1024
    """
    # get the pixel array
    ds = pydicom.dcmread(path, force=True)

    # we have not tested RGB, YBR_FULL, or YBR_FULL_422 yet.
    if ds.PhotometricInterpretation not in ['MONOCHROME1', 'MONOCHROME2']:
        raise NotImplementedError(f'PhotometricInterpretation `{ds.PhotometricInterpretation}` is not yet supported.')

    data = ds.pixel_array
    
    # LUT for human friendly view
    data = pydicom.pixel_data_handlers.util.apply_voi_lut(data, ds, index=0)

    # `MONOCHROME1` have an inverted view; Bones are black; background is white
    # https://web.archive.org/web/20150920230923/http://www.mccauslandcenter.sc.edu/mricro/dicom/index.html
    if ds.PhotometricInterpretation == "MONOCHROME1":
        warnings.warn(f"Coverting MONOCHROME1 to MONOCHROME2 interpretation for file: {path}. Can be avoided by setting `fix_monochrome=False`")
        data = data.max() - data

    # normalize data to [-1024, 1024]
    data = xrv.utils.normalize(data, data.max())
    return data

def get_diagnosis(dicom_path: str)->None:
    """
    Utiliza o modelo pré-treinado do torchxrayvision para classificar a probabilidade de
    patologias da imagem DICOM especificada
    Args:
        dicom_path (str): Caminho do arquivo da imagem DICOM
    Returns:
        dict[str, float]: Dicionário que associa cada patologia à sua probabilidade de existência
    """
    # Prepare the image:
    img = read_xray_dcm(dicom_path)
    # Normalizar imagem
    img = (img - img.min()) / (img.max() - img.min()) * 2048 - 1024

    if len(img.shape) == 2:
        img = img[np.newaxis, ...]

    transform = torchvision.transforms.Compose([xrv.datasets.XRayCenterCrop(),xrv.datasets.XRayResizer(224)])

    img = transform(img)
    img = torch.from_numpy(img)

    # Load model and process image
    model = xrv.models.DenseNet(weights="densenet121-res224-all")
    outputs = model(img[None,...]) # or model.features(img[None,...]) 

    print("Diagnóstico obtido com sucesso!")

    result = dict(zip(model.pathologies,outputs[0].detach().numpy()))
    return convert_float32_to_float(result)
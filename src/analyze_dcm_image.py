import torchxrayvision as xrv
import torch, torchvision
import numpy as np
import pydicom

def convert_float32_to_float(input_dict: dict[str,int])->None:
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

def read_and_adjust_dicom(dicom_path: str)->None:
    # Ler o arquivo DICOM
    dcm = pydicom.dcmread(dicom_path)

    # Extrair a imagem do DICOM
    image = dcm.pixel_array

    # Verificar o valor máximo da imagem
    max_value = np.max(image)
    print(f"Valor máximo da imagem: {max_value}")

    # Redimensionar a imagem se o valor máximo for maior que 4095
    if max_value > 4095:
        print("Redimensionando a imagem para 12 bits.")
        # Normalizar a imagem para o intervalo de 0 a 4095
        image = (image / max_value) * 4095
        image = image.astype(np.uint16)  # Converter para 16 bits

    # Agora você pode usar a função read_xray_dcm
    try:
        # processed_image = xrv.utils.read_xray_dcm(image)
        return image
    except Exception as e:
        raise Exception(f"Erro ao processar a imagem: {e}")

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
    img = read_and_adjust_dicom(dicom_path)
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

    print("Diagnóstico obtido com sucesso!")

    result = dict(zip(model.pathologies,outputs[0].detach().numpy()))
    return convert_float32_to_float(result)

d = get_diagnosis('dicom_samples/id_0a1f875b-a67fe221-684adc8a-39b1c19b-266b948b/Study_22028902.48449501.25544157.65169404.59411193/Series_84639027.32441790.39783484.46756843.74807336/image-37893342-90788293-97674894-30563722-15937211.dcm')
for k, v in d.items():
    print(f"{k}: {v}")
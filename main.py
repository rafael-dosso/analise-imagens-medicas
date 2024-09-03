from send_dicom import post_file
from analyze_dcm_image import get_diagnosis
from pathlib import Path
import numpy as np
import json

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

def main():
    path = Path("dicom_samples")
    dicom_files = path.rglob("*.dcm")  # rglob é usado para buscar arquivos recursivamente
    
    for file_path in dicom_files:
        post_file(file_path)

        with open(str(file_path.parent) + '/diagnosis.json', 'w') as json_file:
            diagnosis = get_diagnosis(file_path)
            convert_float32_to_float(diagnosis)
            json.dump(diagnosis, json_file, indent=4)

if __name__ == "__main__":
    main()
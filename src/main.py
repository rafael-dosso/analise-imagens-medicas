from send_dicom import post_file
from analyze_dcm_image import get_diagnosis
from pathlib import Path
import numpy as np
import json

def main():
    # Lista todos os arquivos .dcm na pasta e aplica as regras de negócio a todos eles
    path = Path("dicom_samples/")
    dicom_files = path.rglob("*.dcm")  # rglob é usado para buscar arquivos recursivamente
    
    for file_path in dicom_files:
        # Sobe o arquivo para o OrthanC
        print(f"Arquivo atual: {file_path}")
        post_file(file_path)

        # Registra um .json com as conslusões do modelo no mesmo diretório do .dcm
        with open(str(file_path.parent) + '/diagnosis.json', 'w') as json_file:
            diagnosis = get_diagnosis(file_path)
            json.dump(diagnosis, json_file, indent=4)
        print("Análise obtida com sucesso!\n")

if __name__ == "__main__":
    main()
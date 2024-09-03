from send_dicom import post_file
from analyze_dcm_image import get_diagnosis
from create_sr import create_sr
from pathlib import Path
import numpy as np
import json

def main():
    # Lista todos os arquivos .dcm na pasta e aplica as regras de negócio a todos eles
    path = Path("dicom_samples/")
    dicom_files = path.rglob("*.dcm")  # rglob é usado para buscar arquivos recursivamente
    
    for file_path in dicom_files:
        if file_path.name == 'structured_report.dcm': continue # Ignora os arquivos SR

        try:
            print('\n====================================\n')
            # Sobe o arquivo para o OrthanC
            print(f"Arquivo atual: {file_path.name}")
            post_file(file_path)

            diagnosis = get_diagnosis(file_path)

            # Registra um .json com as conslusões do modelo no mesmo diretório do .dcm
            file_folder = str(file_path.parent)
            with open(file_folder + '/diagnosis.json', 'w') as json_file:
                json.dump(diagnosis, json_file, indent=4)

            # Cria o SR para a imagem e envia para o Orthanc
            sr_path = file_folder + '/structured_report.dcm'
            create_sr(file_path, sr_path, diagnosis=diagnosis)
            post_file(sr_path)
        except Exception as e:
            print('Ocorreu um erro:', e)

        


        

if __name__ == "__main__":
    main()
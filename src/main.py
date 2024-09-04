from send_dicom import post_file
from analyze_dcm_image import get_diagnosis
from create_sr import create_sr
from pathlib import Path
import numpy as np
import json

def main():
    """
    Lê cada arquivo DICOM da pasta dicom_samples/ e executa os seguintes passos:
        1. Envia-o para o PACs Orthanc;
        2. Analisa sua imagem e obtém um diagnóstico com o modelo pré treinado do
        torchxrayvision, e guarda-o em um json na mesma localização do arquivo;
        3. Cria um DICOM Structured SR para a imagem inicial com os diagnósticos obtidos e
        o envia para o PACs Orthanc;
    """
    # Lista todos os arquivos .dcm na pasta e aplica as regras de negócio a todos eles
    path = Path("dicom_samples/")
    dicom_files = path.rglob("*.dcm")  # rglob é usado para buscar arquivos recursivamente
    
    for file_path in dicom_files:
        if file_path.name == 'structured_report.dcm': continue # Ignora os arquivos SR

        try:
            print('\n============================================\n')
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
            print('Ocorreu um erro com o arquivo. Mensagem de erro:', e)

if __name__ == "__main__":
    main()
import requests

# docker run -p 4242:4242 -p 8042:8042 --rm jodogne/orthanc-plugins

# URL do Orthanc
orthanc_url = 'http://localhost:8042/instances'

# Credenciais
username = 'orthanc'
password = 'orthanc'

def post_file(file_path: str)->None:
    """
    Envia o arquivo especificado para a API do Orthanc
    Args:
        file_path (str): Caminho do arquivo que se deseja enviar
    """

    # Envio do arquivo DICOM ao Orthanc
    with open(file_path, 'rb') as dicom_file:
        response = requests.post(orthanc_url, files={'file': dicom_file}, auth=(username, password))

    if response.status_code >= 200 and response.status_code < 300:
        print("Arquivo enviado com sucesso!")
    else:
        print("Erro ao enviar o arquivo")
        print(response.text)

# dicom_file_path = 'dicom_samples/id_0a0c2c8f-a36a1e82-a4857225-5a2af2a6-c7be16c1/Study_12840378.32185825.64169999.71049659.46899097/Series_60731327.33236805.18319358.84233616.48423037/image-77089611-78785961-69826278-95000740-26294623.dcm'
# sr_destination_path = 'dicom_samples/id_0a0c2c8f-a36a1e82-a4857225-5a2af2a6-c7be16c1/Study_12840378.32185825.64169999.71049659.46899097/Series_60731327.33236805.18319358.84233616.48423037/diagnostic_report_sr.dcm'

# post_file(dicom_file_path)

# create_dicom_sr(dicom_file_path, sr_destination_path)

# post_file('test_report.dcm')
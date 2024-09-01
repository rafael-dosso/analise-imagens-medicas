import requests

# URL do Orthanc
orthanc_url = 'http://localhost:8042/instances'

# Caminho para o arquivo DICOM
dicom_file_path = 'dicom_samples.zip'

# Credenciais
username = 'orthanc'
password = 'orthanc'

# Envio do arquivo DICOM ao Orthanc
with open(dicom_file_path, 'rb') as dicom_file:
    response = requests.post(orthanc_url, files={'file': dicom_file}, auth=(username, password))

if response.status_code >= 200 and response.status_code < 300:
    print("Arquivo enviado com sucesso!")
else:
    print("Erro ao enviar o arquivo")
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

post_file('relatorio_estruturado.dcm')
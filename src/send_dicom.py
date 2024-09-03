import httplib2
import base64

# sudo docker run -p 4242:4242 -p 8042:8042 --rm -v /tmp/orthanc.json:/etc/orthanc/orthanc.json:ro jodogne/orthanc:1.12.4

# URL do Orthanc
orthanc_url = 'http://localhost:8042/instances'

def post_file(file_path: str)->None:
    """
    Envia o arquivo especificado para a API do Orthanc
    Args:
        file_path (str): Caminho do arquivo que se deseja enviar
    """
    headers = { 'content-type' : 'application/dicom' }
    creds_str_bytes = "orthanc:orthanc".encode('ascii')
    creds_str_bytes_b64 = b'Basic ' + base64.b64encode(creds_str_bytes)
    headers['authorization'] = creds_str_bytes_b64.decode('ascii')

    with open(file_path, 'rb') as dicom_file:
        resp, content = httplib2.Http().request(orthanc_url, 'POST', 
                                    body = dicom_file.read(),
                                    headers = headers)

    if resp.status >= 200 and resp.status < 300:
        # Guardar as informações da instância
        print('Arquivo enviado com sucesso!')
    else:
        print('Houve um erro ao enviar o arquivo.')
        print(resp)
        print(content)
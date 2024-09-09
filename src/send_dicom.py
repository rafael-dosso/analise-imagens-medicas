import httplib2
import base64

def post_file(file_path: str, api_address: str)->None:
    """
    Envia o arquivo especificado para a API do Orthanc
    Args:
        file_path (str): Caminho do arquivo que se deseja enviar
        api_address (str): Caminho da API do Orthanc
    """
    orthanc_url = api_address + '/instances'

    headers = { 'content-type' : 'application/dicom' }
    creds_str_bytes = "orthanc:orthanc".encode('ascii') # Credenciais de autenticação no formato usuario:senha. Se substitua se necessario
    creds_str_bytes_b64 = b'Basic ' + base64.b64encode(creds_str_bytes)
    headers['authorization'] = creds_str_bytes_b64.decode('ascii')

    # Envia a requisição POST para a API
    with open(file_path, 'rb') as dicom_file:
        resp, content = httplib2.Http().request(orthanc_url, 'POST', 
                                    body = dicom_file.read(),
                                    headers = headers)

    if resp.status >= 200 and resp.status < 300:
        print('Arquivo enviado com sucesso!')
    else:
        print('Houve um erro ao enviar o arquivo.')
        print(content)

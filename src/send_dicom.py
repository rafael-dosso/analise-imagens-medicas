import httplib2
import json
import pydicom

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

    with open(file_path, 'rb') as dicom_file:
        resp, content = httplib2.Http().request(orthanc_url, 'POST', 
                                    body = dicom_file.read(),
                                    headers = headers)

    if resp.status >= 200 and resp.status < 300:
        # Guardar as informações da instância
        print('Arquivo enviado com sucesso!')
        response_body = json.loads(content)
        print(response_body)
        # id = response_body['ID']

        # if id:
        #     print('SOPInstanceUID gerado:', id)
        #     dcm = pydicom.dcmread(file_path)
        #     print(dcm.SOPInstanceUID)
        #     dcm.SOPInstanceUID = id.replace('-', '.')
        # else:
        #     print("Não foi gerado um SOPInstanceUID para o arquivo")

    else:
        print('Houve um erro ao enviar o arquivo.')
        print(resp)
        print(content)

post_file('relatorio_estruturado.dcm')
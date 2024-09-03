import httplib2

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

    if resp.status == 200:
        # Guardar as informações da instancia
        print('Arquivo enviado com sucesso!')
        print(resp)
        print(content)
    else:
        print('Houve um erro ao enviar o arquivo.')
        print(resp)
        print(content)

post_file('dicom_samples/id_0a1f875b-a67fe221-684adc8a-39b1c19b-266b948b/Study_22028902.48449501.25544157.65169404.59411193/Series_57322992.77011198.27473253.16855266.10345337/image-43591434-24105909-95501830-31186664-56232345.dcm')
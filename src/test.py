import pydicom
from pydicom.dataset import Dataset, FileDataset
from datetime import datetime

# Lê o arquivo original para usar suas informações no cabeçalho do SR
dcm = pydicom.dcmread('dicom_samples/id_0a1f875b-a67fe221-684adc8a-39b1c19b-266b948b/Study_22028902.48449501.25544157.65169404.59411193/Series_57322992.77011198.27473253.16855266.10345337/image-43591434-24105909-95501830-31186664-56232345.dcm')

# Criar um novo conjunto de dados com um cabeçalho de arquivo DICOM
file_meta = dcm.file_meta

# Criar um novo conjunto de dados DICOM
ds = FileDataset("relatorio_estruturado.dcm", {}, file_meta=file_meta, preamble=b"\0" * 128)

# Definir as propriedades de codificação
ds.is_little_endian = True
ds.is_implicit_VR = True

# Adicionar metadados básicos
ds.PatientName = "Nome do Paciente"
ds.PatientID = "ID do Paciente"
ds.StudyInstanceUID = "1.2.3.4.5"
ds.SeriesInstanceUID = "1.2.3.4.5.6"
ds.SOPInstanceUID = "1.2.3.4.5.6.7"
ds.SOPClassUID = "1.2.840.10008.5.1.4.1.1.88.22"  # UID para DICOM SR

# Adicionar data e hora
dt = datetime.now()
ds.StudyDate = dt.strftime('%Y%m%d')
ds.StudyTime = dt.strftime('%H%M%S')

# Criar um novo Dataset para o conteúdo do relatório
content_item = Dataset()
content_item.ValueType = "TEXT"
content_item.ConceptNameCodeSequence = [Dataset()]
content_item.ConceptNameCodeSequence[0].CodeValue = "121072"
content_item.ConceptNameCodeSequence[0].CodingSchemeDesignator = "DCM"
content_item.ConceptNameCodeSequence[0].CodeMeaning = "Observação"
content_item.TextValue = "Este é um exemplo de relatório estruturado."

# Adicionar o item de conteúdo à sequência
ds.ContentSequence = [content_item]

# Definir o caminho do arquivo
output_file = "relatorio_estruturado.dcm"

# Salvar o conjunto de dados em um arquivo DICOM
ds.save_as(output_file)

# Ler o arquivo DICOM criado
ds_read = pydicom.dcmread(output_file)
print(ds_read)
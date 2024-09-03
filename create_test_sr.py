import pydicom
from pydicom.dataset import Dataset, FileDataset
from datetime import datetime

# Criar um novo conjunto de dados com um cabeçalho de arquivo DICOM
file_meta = Dataset()
file_meta.MediaStorageSOPClassUID = "1.2.840.10008.5.1.4.1.1.88.22"  # UID para DICOM SR
file_meta.MediaStorageSOPInstanceUID = "1.2.3.4.5.6.7"
file_meta.ImplementationClassUID = "1.2.3.4"
file_meta.TransferSyntaxUID = pydicom.uid.ImplicitVRLittleEndian

# Criar um novo conjunto de dados DICOM
ds = FileDataset("relatorio_estruturado.dcm", {}, file_meta=file_meta, preamble=b"\0" * 128)

# Definir as propriedades de codificação
ds.is_little_endian = True
ds.is_implicit_VR = True

# Definir o cabeçalho do metafile DICOM
ds.file_meta.MediaStorageSOPClassUID = "1.2.840.10008.5.1.4.1.1.88.22"
ds.file_meta.MediaStorageSOPInstanceUID = "1.2.3.4.5.6.7"
ds.file_meta.ImplementationClassUID = "1.2.3.4"

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
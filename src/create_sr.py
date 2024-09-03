import pydicom
from pydicom.dataset import Dataset, FileDataset
from pydicom.uid import generate_uid
from datetime import datetime
from analyze_dcm_image import get_diagnosis

# original_dicom = pydicom.dcmread('dicom_samples/id_0a1f875b-a67fe221-684adc8a-39b1c19b-266b948b/Study_22028902.48449501.25544157.65169404.59411193/Series_57322992.77011198.27473253.16855266.10345337/image-43591434-24105909-95501830-31186664-56232345.dcm')

def create_sr(dicom_path:str)->None:
    # Lê o arquivo original para usar suas informações no cabeçalho do SR
    dcm = pydicom.dcmread(dicom_path)

    # Criar um novo conjunto de dados com um cabeçalho de arquivo DICOM
    file_meta = Dataset()
    file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.88.22'  # Enhanced SR Storage
    file_meta.MediaStorageSOPInstanceUID = generate_uid()
    file_meta.ImplementationClassUID = generate_uid()
    file_meta.TransferSyntaxUID = pydicom.uid.ImplicitVRLittleEndian

    # Criar um novo conjunto de dados DICOM
    sr = FileDataset("relatorio_estruturado.dcm", {}, file_meta=file_meta, preamble=b"\0" * 128)

    # Definir as propriedades de codificação
    sr.is_little_endian = True
    sr.is_implicit_VR = True

    # Adicionar metadados básicos
    sr.PatientName = dcm.PatientName
    sr.PatientID = dcm.PatientID
    sr.StudyInstanceUID = dcm.StudyInstanceUID
    sr.SeriesInstanceUID = dcm.SeriesInstanceUID
    sr.SOPInstanceUID = generate_uid()
    sr.SOPClassUID = '1.2.840.10008.5.1.4.1.1.88.22' # Enhanced SR Storage

    # Adicionar data e hora
    dt = datetime.now()
    sr.StudyDate = dt.strftime('%Y%m%d')
    sr.StudyTime = dt.strftime('%H%M%S')

    # Criar um novo Dataset para o conteúdo do relatório
    content_item = Dataset()
    content_item.ValueType = "TEXT"
    content_item.ConceptNameCodeSequence = [Dataset()]
    content_item.ConceptNameCodeSequence[0].CodeValue = "121072"
    content_item.ConceptNameCodeSequence[0].CodingSchemeDesignator = "DCM"
    content_item.ConceptNameCodeSequence[0].CodeMeaning = "Observação"
    content_item.TextValue = "Este é um exemplo de relatório estruturado."

    diagnosis = get_diagnosis(dicom_path)

    # Criar uma lista para armazenar os itens de conteúdo
    content_items = []

    # Adicionar cada patologia e sua probabilidade ao conteúdo
    for pathology, probabilty in diagnosis.items():
        content_item = Dataset()
        content_item.ValueType = "TEXT"
        content_item.ConceptNameCodeSequence = [Dataset()]
        content_item.ConceptNameCodeSequence[0].CodeValue = "121072"  # Código genérico para Observação
        content_item.ConceptNameCodeSequence[0].CodingSchemeDesignator = "DCM"
        content_item.ConceptNameCodeSequence[0].CodeMeaning = pathology
        content_item.TextValue = f"Probabilidade: {probabilty:.2f}"  # Formatar a probabilidade com duas casas decimais
        
        # Adicionar o item de conteúdo à lista
        content_items.append(content_item)

    # Adicionar o item de conteúdo à sequência
    sr.ContentSequence = [content_item]

    # Definir o caminho do arquivo
    output_file = "relatorio_estruturado.dcm"

    # Salvar o conjunto de dados em um arquivo DICOM
    sr.save_as(output_file)
    print(f"Structured Report salvo em: {output_file}")

create_sr("dicom_samples/id_0a1a0de9-947c36de-38f2e3c9-a497807e-7ceb75f8/Study_72682317.56696215.32367375.69516389.09416010/Series_94559003.83259051.98386686.73459116.65935633/image-49456968-50961677-93916823-30114741-97249659.dcm")

# Ler o arquivo DICOM criado
sr_read = pydicom.dcmread("relatorio_estruturado.dcm")
print(sr_read)
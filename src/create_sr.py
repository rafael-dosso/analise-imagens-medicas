import pydicom
from pydicom.dataset import Dataset, FileDataset
from pydicom.uid import generate_uid
from datetime import datetime
from analyze_dcm_image import get_diagnosis

# original_dicom = pydicom.dcmread('dicom_samples/id_0a1f875b-a67fe221-684adc8a-39b1c19b-266b948b/Study_22028902.48449501.25544157.65169404.59411193/Series_57322992.77011198.27473253.16855266.10345337/image-43591434-24105909-95501830-31186664-56232345.dcm')

def create_sr(dicom_path:str, sr_output_path: str, diagnosis=None)->None:
    """
    Gera um DICOM Structured Report com base no diagnóstico obtido pelo modelo a partir
    da imagem DICOM fornecida.
    Args:
        dicom_path (str): Caminho da imagem a ser analizada
        sr_output_path (str): Caminho em que será guardado o relatório
        diagnosis (dict[str, int]): Parâmetro opcional para anexar o dicionário do diagnóstico se ele já foi obtido
    """
    # Lê o arquivo original para usar suas informações no cabeçalho do SR
    dcm = pydicom.dcmread(dicom_path)

    # Criar um novo conjunto de dados com um cabeçalho de arquivo DICOM
    file_meta = Dataset()
    file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.88.22'  # Enhanced SR Storage
    file_meta.MediaStorageSOPInstanceUID = generate_uid()
    file_meta.ImplementationClassUID = generate_uid()
    file_meta.TransferSyntaxUID = pydicom.uid.ImplicitVRLittleEndian

    # Criar um novo conjunto de dados DICOM
    sr = FileDataset(sr_output_path, {}, file_meta=file_meta, preamble=b"\0" * 128)

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

    # Obtém o diagnóstico se ele não foi gerado ainda
    if not diagnosis:
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
        content_item.MeasuredValueSequence = [Dataset()]
        content_item.MeasuredValueSequence[0].MeasurementUnitsCodeSequence = [Dataset()]
        content_item.MeasuredValueSequence[0].MeasurementUnitsCodeSequence[0].CodeMeaning = "Probability of pathology in percentage"
        content_item.MeasuredValueSequence[0].NumericValue = f'{probabilty*100:.2f}'
        
        # Adicionar o item de conteúdo à lista
        content_items.append(content_item)

    # Adicionar o item de conteúdo à sequência
    sr.ContentSequence = content_items

    # Salvar o conjunto de dados em um arquivo DICOM
    sr.save_as(sr_output_path)
    print(f"Structured Report salvo em: {sr_output_path}")
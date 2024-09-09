import pydicom
from pydicom.dataset import Dataset, FileDataset
from pydicom.uid import generate_uid
from datetime import datetime
from analyze_dcm_image import get_diagnosis

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

    # Adicionar dados do cabecalho
    sr.PatientName = dcm.PatientName
    sr.PatientID = dcm.PatientID
    sr.StudyInstanceUID = dcm.StudyInstanceUID
    sr.SeriesInstanceUID = dcm.SeriesInstanceUID
    sr.SOPInstanceUID = generate_uid()
    sr.SOPClassUID = '1.2.840.10008.5.1.4.1.1.88.22' # Enhanced SR Storage

    # Adicionar campos do módulo "General Study"
    now = datetime.now()
    sr.AccessionNumber = f'AN{now.year}-{now.month}-{now.day}-000'
    sr.StudyID = f'SR{now.year}-{now.month}-{now.day}-000'  # Tag (0020,0010)

    # Adicionar campos do módulo "SR Document General"
    sr.InstanceNumber = str(int(dcm.InstanceNumber) + 1)  # Tag (0020,0013)
    sr.CompletionFlag = "COMPLETE"  # Tag (0040,A491)
    sr.VerificationFlag = "UNVERIFIED"  # Tag (0040,A493)

    # Adicionar campos do módulo "SR Document Series"
    sr.Modality = "SR"  # Tag (0008,0060)
    sr.SeriesNumber = dcm.SeriesNumber  # Tag (0020,0011)

    # Adicionar data e hora
    dt = datetime.now()
    sr.StudyDate = dt.strftime('%Y%m%d')
    sr.StudyTime = dt.strftime('%H%M%S')
    sr.ContentDate = datetime.now().strftime('%Y%m%d')  # Tag (0008,0023)
    sr.ContentTime = datetime.now().strftime('%H%M%S')  # Tag (0008,0033)

    sr.StudyDescription = f'Diagnosis obtained over original image with InstanceNumber {dcm.InstanceNumber}'
    sr.ProtocolName = dcm.ProtocolName

    # Adiciona um pequeno cabeçalho para os dados
    sr.ConceptNameCodeSequence = [Dataset()]
    sr.ConceptNameCodeSequence[0].CodeValue = "121072"
    sr.ConceptNameCodeSequence[0].CodingSchemeDesignator = 'DCM'
    sr.ConceptNameCodeSequence[0].CodeMeaning = 'Diagnosis Percentages'

    # Obtém o diagnóstico se ele não foi gerado ainda
    if not diagnosis:
        diagnosis = get_diagnosis(dicom_path)

    # Criar uma lista para armazenar os itens de conteúdo
    content_items = []

    # Adicionar cada patologia e sua probabilidade ao conteúdo
    for pathology, probabilty in diagnosis.items():
        content_item = Dataset()
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

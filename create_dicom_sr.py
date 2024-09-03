import pydicom
from pydicom.dataset import Dataset, FileDataset
from analyze_dcm_image import get_diagnosis
import datetime

def create_dicom_sr(dicom_file_path: str, sr_destination_path: str) -> None:
    """ 
    Cria um SR baseado nos resultados encontrados pelo modelo pré-treinado
    Args:
        dicom_file_path (str): Caminho do arquivo DICOM para o qual será escrito o SR
        sr_destination_path (str): Caminho em que será armazenado o SR
    """

    # Analisa a imagem para obter os resultados do modelo
    diagnosis = get_diagnosis(dicom_file_path)
    print("Diagnósticos obtidos com sucesso")

    # Carregar o arquivo DICOM existente
    ds = pydicom.dcmread(dicom_file_path)

    # Criar um novo Dataset para o Structured Report
    sr_ds = FileDataset(sr_destination_path, {}, file_meta=ds.file_meta, preamble=b"\0" * 128)

    # Definir informações básicas do SR
    sr_ds.SOPClassUID = '1.2.840.10008.5.1.4.1.1.88.22'
    sr_ds.SOPInstanceUID = pydicom.uid.generate_uid()
    sr_ds.PatientName = ds.PatientName
    sr_ds.PatientID = ds.PatientID
    sr_ds.StudyInstanceUID = ds.StudyInstanceUID
    sr_ds.SeriesInstanceUID = pydicom.uid.generate_uid()
    sr_ds.Modality = "SR"
    sr_ds.StudyDate = ds.StudyDate
    sr_ds.ContentDate = datetime.date.today().strftime('%Y%m%d')
    sr_ds.ContentTime = datetime.datetime.now().strftime('%H%M%S')

    # Criar a estrutura do SR
    sr_content = Dataset()
    sr_content.ContentSequence = pydicom.Sequence([])

    for pathology, probability in diagnosis.items():
        content_item = Dataset()
        content_item.ValueType = "TEXT"
        content_item.ConceptNameCodeSequence = pydicom.Sequence([Dataset()])
        content_item.ConceptNameCodeSequence[0].CodeValue = "123004"  # Código fictício para o diagnóstico
        content_item.ConceptNameCodeSequence[0].CodingSchemeDesignator = "SRT"
        content_item.ConceptNameCodeSequence[0].CodeMeaning = pathology
        content_item.TextValue = f"{pathology}: {probability * 100:.2f}%"

        # Adiciona o item de conteúdo à sequência como um Dataset
        sr_content.ContentSequence.append(content_item)

    # Adicionar os itens de conteúdo ao SR
    sr_ds.ContentSequence = pydicom.Sequence(sr_content.ContentSequence)

    # Salvar o Structured Report em um arquivo DICOM
    sr_ds.save_as(sr_destination_path)
    print(f"Structured Report salvo em: {sr_destination_path}")
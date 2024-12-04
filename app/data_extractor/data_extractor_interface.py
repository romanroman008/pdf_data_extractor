from abc import ABC, abstractmethod

from PyPDF2 import PdfReader


class IDataExtractor(ABC):

    @abstractmethod
    def extract(self, pdf_path):
        pass


import logging
import re
from typing import Optional, List
from PyPDF2 import PdfReader


from app.data_extractor.data_extractor_interface import IDataExtractor
from app.data_extractor.exceptions.InvalidOwnershipTypeException import InvalidOwnershipTypeException
from app.data_extractor.ownership_factory.ownership_dispatcher import OwnershipDispatcher
from app.model.ownership.ownership import Ownership


class LandRegisterDataExtractor(IDataExtractor):
    def __init__(self, ownership_factory: OwnershipDispatcher, logger: logging.Logger):
        self.logger = logger
        self.ownership_factory = ownership_factory

    def extract(self, pdf_path: str) -> Optional[List[Ownership]]:
        self.logger.info(f"Starting extraction from PDF: {pdf_path}")
        try:
            with open(pdf_path, 'rb') as file:
                self.logger.debug(f"Opened file: {pdf_path}")
                reader = PdfReader(file)
                text = ""
                for page_number, page in enumerate(reader.pages):
                    page_text = page.extract_text()
                    if page_text:
                        self.logger.debug(f"Extracted text from page {page_number + 1}")
                        text += page_text
                    else:
                        self.logger.warning(f"Page {page_number + 1} has no extractable text")

                # Split the text into sections
                sections = self.__split_text_by_case_and_page(text)
                self.logger.debug(f"Split text into {len(sections)} sections")

                results = self.create_ownerships(sections)
                self.logger.info(f"Extraction complete for {pdf_path}, extracted {len(results)} ownership records")
                return results

        except FileNotFoundError as e:
            self.logger.error(f"File not found: {pdf_path} - {e}")
        except Exception as e:
            self.logger.critical(f"Error extracting data from {pdf_path}: {str(e)}", exc_info=True)
        return None

    def create_ownerships(self, sections):
        results = []
        for section_number, section in enumerate(sections):
            self.logger.debug(f"Processing section {section_number + 1}")
            try:
                # Attempt to create ownerships for this section
                ownerships = self.ownership_factory.dispatch_ownership_creation(section)
                results.extend(ownerships)
            except InvalidOwnershipTypeException as e:
                # Log the error and problematic page
                self.logger.error(
                    f"Error processing section {section_number + 1}: {str(e)}"
                )
                self.logger.debug(f"Problematic section content: {section}")
                # Skip this section and continue with the next one
                continue

        return results

    def __split_text_by_case_and_page(self, text: str) -> List[str]:
        self.logger.debug("Splitting text by case and page")
        pattern = re.compile(r"(nazwa organu wydającego dokument.*?Strona \d+ z \d+)", re.DOTALL)
        sections = pattern.findall(text)
        self.logger.debug(f"Found {len(sections)} sections")
        return sections

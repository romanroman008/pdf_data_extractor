import logging
import os
import re

from app.data_extractor.land_register_data_extractor import LandRegisterDataExtractor
from app.document_generator.company_document import CompanyDocument
from app.document_generator.private_document import PrivateDocument
from app.model.investor import Investor
from app.model.ownership.ownership_kind import OwnershipKind


class PDFProcessingController:
    def __init__(self,land_register_extractor: LandRegisterDataExtractor, logger: logging.Logger):
        self.land_register_extractor = land_register_extractor
        self.logger = logger
        self.investor = None  # Will be set when processing the PDF

    def process_pdf(self, pdf_path, project_name, type_of_work, directory):
        # Create the investor with user inputs

        self.investor = self._generate_investor(project_name, type_of_work)

        ownership_list = self.land_register_extractor.extract(pdf_path)

        if not ownership_list:
            return False
        for ownership in ownership_list:
            self._generate_document_for_ownership(ownership, directory)
        return True

    def _generate_document_for_ownership(self, ownership, directory):
        if ownership.get_kind() == OwnershipKind.PRIVATE:
            document = PrivateDocument(ownership, self.investor)
        elif ownership.get_kind() == OwnershipKind.COMPANY:
            document = CompanyDocument(ownership, self.investor)
        else:
            raise ValueError(f"Unknown ownership kind: {ownership.get_kind()}")

        # Automatically save the file in the selected directory
        output_filename = self._generate_output_filename(ownership, directory)
        if output_filename:
            document.generate(output_filename)

    def _generate_output_filename(self, ownership, directory):

        # Fetch the name from ownership
        name = ownership.get_name()  # This should now be a string

        # If for any reason name is not a string, convert it to a string to avoid issues
        if not isinstance(name, str):
            raise ValueError(f"Expected a string for name, but got {type(name)}")

        # Clean the name for any invalid characters and replace spaces with underscores
        valid_name = re.sub(r'[\\/*?:"<>|\n]', '_', name.replace(" ", "_"))

        # Create the filename with a .docx extension (or change to .pdf if needed)
        filename = f"{valid_name}_ownership.docx"

        # Return the full output file path
        return os.path.join(directory, filename)

    def _generate_investor(self, project_name, type_of_work):
        name = "ENEA Operator sp. z o.o."
        address = "Poznań przy ul. Strzeszyńska 58, Oddział Dystrybucji w Bydgoszcz, Rejon Dystrybucji Chojnice"
        # Use the inputs passed from the PDFApp
        name_of_work = project_name
        return Investor(name, address, type_of_work, name_of_work)

from typing import Optional, List

from app.data_extractor.ownership_factory.ownership_factory import OwnershipFactory
from app.data_extractor.regex.RegexPatterns import RegexPatterns

from app.model.ownership.company_ownership import CompanyOwnership
from app.model.ownership.ownership import Ownership


class CompanyOwnershipFactory(OwnershipFactory):

    def create_ownership(self, section: str) -> List[Ownership]:

        self.logger.debug("Creating CompanyOwnership")
        page_number = self._find_page_info(section)
        # Extract necessary data
        try:
            name = self.__find_company_name(section)
            address = self.__find_company_address(section)
            nob = self.__find_nob(section)
            tin = self.__find_tin(section)
            reg_unit = self._find_reg_unit(section)
            circle = self._find_circle(section)
            parcel_number = self._find_parcel_number(section)
            land_register = self._find_land_register(section)

            # Validate critical fields
            if not name or not nob:
                self._log_missing_critical_data(page_number, section, name=name, NOB=nob)
                return []

                # Create and return the CompanyOwnership object
            company_ownership = CompanyOwnership(name, address, reg_unit, circle, parcel_number, land_register, nob,
                                                 tin)
            self.logger.info(f"Successfully created CompanyOwnership for section {page_number}: {company_ownership}")
            return [company_ownership]

        except Exception as e:
            self.logger.error(f"Error creating CompanyOwnership for section {page_number}: {e}", exc_info=True)
            return []

    def __find_company_name(self, text: str) -> Optional[str]:
        return self._find_field("company name", RegexPatterns.COMPANY_NAME, text)

    def __find_company_address(self, text: str) -> Optional[str]:
        return self._find_field("company address", RegexPatterns.COMPANY_ADDRESS, text)

    def __find_nob(self, text: str) -> Optional[str]:
        nob = self._find_field("NOB", RegexPatterns.NOB, text)
        if nob:
            return nob.replace(" ", "_")
        else:
            return None

    def __find_tin(self, text: str) -> Optional[str]:
        tin = self._find_field("TIN", RegexPatterns.TIN, text)
        if tin:
            return tin.replace(" ", "_")
        else:
            return None

from abc import abstractmethod, ABC
from typing import Optional

import logging

from app.data_extractor.regex.RegexPatterns import RegexPatterns
from app.data_extractor.regex.RegexUtils import RegexUtils


class OwnershipFactory(ABC):
    def __init__(self, logger: logging.Logger):
        self.logger = logger

    @abstractmethod
    def create_ownership(self, section:str):
        pass

    def _find_page_info(self, text: str):
        pattern = RegexPatterns.PAGE_INFO
        match = RegexUtils.match_pattern(pattern, text)
        if match:
            self.logger.debug(f"Page info found:{match}")
            return match

        self.logger.warning("Page information not found in the text.")
        return None

    def _find_field(self, field_name: str, pattern: str, text: str) -> Optional[str]:
        self.logger.debug(f"Finding {field_name}")

        result = RegexUtils.match_pattern(pattern, text)
        if result:
            self.logger.debug(f"Found {field_name}: {result}")
            return result

        self.logger.info(f"{field_name.capitalize()} not found in text")
        return None

    def _find_land_register(self, text: str) -> Optional[str]:

        return self._find_field("land register", RegexPatterns.LAND_REGISTER, text)

    def _find_parcel_number(self, text: str) -> Optional[str]:
        parcel_number = self._find_field("parcel number", RegexPatterns.PARCEL_NUMBER, text)

        if parcel_number:
            return self._find_field("parcel number additional", RegexPatterns.PARCEL_NUMBER_ADDITIONAL, text)

    def _find_reg_unit(self, text: str) -> Optional[str]:
        reg_unit = self._find_field("registration unit", RegexPatterns.REGISTRATION_UNIT, text)

        if reg_unit:
            return self._find_field("registration unit additional", RegexPatterns.REGISTRATION_UNIT_ADDITIONAL, text)

    def _find_circle(self, text: str) -> Optional[str]:
        return self._find_field("circle", RegexPatterns.CIRCLE, text)

    def _log_missing_critical_data(self, section_number: int, section: str, **missing_fields):

        missing_info = ", ".join([f"{field}={value}" for field, value in missing_fields.items() if not value])
        page = self._find_page_info(section)
        page_info = f"current page: {page[0]}, total pages: {page[1]}" if page else "page info not available"

        self.logger.warning(
            f"Missing critical company data ({missing_info}) in section {section_number}: {section[:100]}... ({page_info})"
        )

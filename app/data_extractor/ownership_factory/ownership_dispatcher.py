import logging
from typing import List

from app.data_extractor.exceptions.InvalidOwnershipTypeException import InvalidOwnershipTypeException
from app.data_extractor.ownership_factory.company_ownership_factory import CompanyOwnershipFactory
from app.data_extractor.ownership_factory.private_ownership_factory import PrivateOwnershipFactory
from app.data_extractor.regex.RegexPatterns import RegexPatterns
from app.data_extractor.regex.RegexUtils import RegexUtils
from app.model.ownership.ownership import Ownership


class OwnershipDispatcher:
    def __init__(self, private_factory: PrivateOwnershipFactory, company_factory: CompanyOwnershipFactory,
                 logger: logging.Logger):
        self.logger = logger
        self.__private_factory = private_factory
        self.__company_factory = company_factory

    def dispatch_ownership_creation(self, section: str) -> List[Ownership]:
        ownership_kind = self.__determine_ownership_type(section)
        self.logger.debug(f"Determined ownership type: {ownership_kind}")

        if ownership_kind == "PRIVATE":
            return self.__private_factory.create_ownership(section)
        elif ownership_kind == "COMPANY":
            return self.__company_factory.create_ownership(section)
        else:
            self.logger.error(f"Unknown ownership type: {ownership_kind}")
            raise InvalidOwnershipTypeException(ownership_kind)

    def __determine_ownership_type(self, text: str) -> str:
        self.logger.debug("Determining ownership kind")

        # Find private matches
        private_matches = RegexUtils.find_all(RegexPatterns.PRIVATE_OWNERSHIP_TYPE, text)

        # Find company matches from two patterns and combine them
        company_matches = (
                RegexUtils.find_all(RegexPatterns.COMPANY_OWNERSHIP_TYPE, text) +
                RegexUtils.find_all(RegexPatterns.COMPANY_OWNERSHIP_TYPE_NO_REGON, text)
        )

        # Determine ownership type based on pattern matches
        if private_matches:
            self.logger.debug(f"Private ownership detected: {private_matches}")
            return "PRIVATE"

        if company_matches:
            self.logger.debug(f"Company ownership detected: {company_matches}")
            return "COMPANY"

        # Fallback if no patterns match
        self.logger.warning("Unable to determine ownership type from the text")
        return "UNKNOWN"



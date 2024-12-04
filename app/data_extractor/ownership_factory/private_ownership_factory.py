import re
from typing import List

from app.data_extractor.ownership_factory.ownership_factory import OwnershipFactory
from app.data_extractor.regex.RegexPatterns import RegexPatterns
from app.data_extractor.regex.RegexUtils import RegexUtils
from app.model.owner import Owner
from app.model.ownership.ownership import Ownership
from app.model.ownership.private_ownership import PrivateOwnership


class PrivateOwnershipFactory(OwnershipFactory):

    def create_ownership(self, section: str) -> List[Ownership]:
        self.logger.debug("Creating PrivateOwnership")

        owner_part = self.__resolve_part_with_ownership(section)
        owners = self.__find_owners(owner_part)

        reg_unit = self._find_reg_unit(section)
        circle = self._find_circle(section)
        parcel_number = self._find_parcel_number(section)
        land_register = self._find_land_register(section)

        # Check for missing critical data
        if not owners:
            page = self._find_page_info(section)
            if page:
                current_page, total_pages = page
                self.logger.warning(
                    f"Missing critical private ownership data (name or SSN) in section: {owners}..., current page: {current_page}, total pages: {total_pages}")
            else:
                self.logger.warning(
                    f"Missing critical private ownership data (name or SSN) in section: {owners}..., page info not available")
            return None  # Skip ownership creation

        ownership_list = []

        for owner in owners:
            ownership_list.append(
                PrivateOwnership(owner.name, owner.ssn, owner.address, reg_unit, circle, parcel_number, land_register))

        # Create and return the PrivateOwnership object
        return ownership_list

    def __resolve_part_with_ownership(self, section):
        try:
            self.logger.info("Starting extraction between 'własność' and 'Działki ewidencyjne'.")
            match = RegexUtils.match_pattern(RegexPatterns.OWNERSHIP_SECTION, section)

            if match:
                self.logger.info("Successfully extracted the text between 'własność' and 'Działki ewidencyjne'.")
                return match
            else:
                self.logger.warning("'własność' or 'Działki ewidencyjne' not found in the text.")
                return None
        except Exception as e:
            self.logger.error(f"An error occurred during extraction: {e}", exc_info=True)
            return None

    def __find_owners(self, text: str) -> List[Owner]:
        self.logger.info("Starting extraction of owners.")
        pattern = RegexPatterns.PRIVATE_OWNERSHIP

        matches = RegexUtils.find_all_named_groups(pattern, text)
        if not matches:
            self.logger.info("No owners found in the text.")
            return []

        owners = []
        for match in matches:
            name = match["name"].strip()
            raw_ssn = match.get("ssn")  # PESEL may be optional
            ssn = re.sub(r"\s+", "", raw_ssn) if raw_ssn else None
            address = match["address"].strip()

            owner = Owner(name=name, ssn=ssn, address=address)
            owners.append(owner)
            self.logger.debug(f"Extracted owner: {owner}")

        self.logger.info(f"Extracted {len(owners)} owners from the text.")
        return owners

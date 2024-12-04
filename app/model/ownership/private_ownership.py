from app.model.ownership.ownership import Ownership
from app.model.ownership.ownership_kind import OwnershipKind


class PrivateOwnership(Ownership):

    def __init__(self, name, ssn, address, reg_unit: str, circle: str, parcel_number: str, land_register: str):
        # Pass None for name, as we're using multiple owners
        super().__init__(name, address, reg_unit, circle, parcel_number, land_register)
        self.ssn = ssn

    def get_details(self):
        return self.ssn

    def get_kind(self):
        return OwnershipKind.PRIVATE

    def get_address(self) -> str:
        return self.address

    def __str__(self) -> str:
        owner_details = ", ".join([owner.get_details() for owner in self.owners])
        return (f"Właściciele: {self.owners}, adres: {self.address}, "
                f"Numer księgi wieczystej: {self.land_register}, Jednostka ewidencyjna: {self.reg_unit}, "
                f"Obręb: {self.circle}, Numer działki: {self.parcel_number}")

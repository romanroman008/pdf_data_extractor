from typing import Optional

from app.model.ownership.ownership import Ownership
from app.model.ownership.ownership_kind import OwnershipKind


class CompanyOwnership(Ownership):
    def __init__(self, name, address: str, reg_unit: str, circle: str, parcel_number: str, land_register: str, nob: str, tin: Optional[str] = None):
        super().__init__(name, address, reg_unit, circle, parcel_number, land_register)
        self.nob = nob
        self.tin = tin

    def get_kind(self):
        return OwnershipKind.COMPANY

    def get_details(self):
        tin_detail = f"NIP: {self.tin}" if self.tin else "NIP: not available"
        return f"REGON: {self.nob}, {tin_detail}"

    def __str__(self):
     # This works if owners is a list of Owner objects
        tin_str = self.tin if self.tin else "not available"
        return (f"Nazwa: {self.name}, Siedziba: {self.address}, REGON: {self.nob}, "
                f"NIP: {tin_str}, Numer księgi wieczystej: {self.land_register}, "
                f"Jednostka ewidencyjna: {self.reg_unit}, Obręb: {self.circle}, Numer działki: {self.parcel_number}")

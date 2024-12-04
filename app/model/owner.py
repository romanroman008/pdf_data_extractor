from typing import Optional


class Owner:
    def __init__(self, name: str, ssn: Optional[str] = None, address: Optional[str] = None, nob: Optional[str] = None,
                 nip: Optional[str] = None):
        self.name = name
        self.address = address
        self.ssn = ssn  # PESEL or personal identifier, optional for companies
        self.nob = nob  # Optional, used for companies
        self.nip = nip  # Optional, used for companies

    def get_details(self) -> str:
        """Returns a formatted string of the owner's details."""
        details = f"Name: {self.name}"
        if self.ssn:
            details += f" (PESEL: {self.ssn})"
        if self.address:
            details += f", Address: {self.address}"
        if self.nob:
            details += f", REGON: {self.nob}"
        if self.nip:
            details += f", NIP: {self.nip}"
        return details

    def __str__(self):
        """String representation of the Owner object."""
        return self.get_details()

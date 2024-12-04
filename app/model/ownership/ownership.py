from abc import ABC, abstractmethod




class Ownership(ABC):
    def __init__(self, name, address, reg_unit, circle, parcel_number, land_register):
        self.name = name
        self.address = address
        self.reg_unit = reg_unit
        self.circle = circle
        self.parcel_number = parcel_number
        self.land_register = land_register

    @abstractmethod
    def get_kind(self):
        pass

    def get_name(self):
        """
        Returns the name of the ownership (which should be a string).
        """
        # Ensure the name is always returned as a string
        return str(self.name)  # Convert to string if necessary, but assuming it's already a string

    def get_address(self):
        return self.address

    @abstractmethod
    def get_details(self):
        pass

    def get_circle(self):
        return self.circle

    def get_parcel_number(self):
        return self.parcel_number

    def get_reg_unit(self):
        return self.reg_unit

    def get_land_register(self):
        return self.land_register

    @abstractmethod
    def __str__(self):
        pass

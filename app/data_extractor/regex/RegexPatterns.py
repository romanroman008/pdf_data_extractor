class RegexPatterns:
    """
    A centralized class for storing regex patterns.
    Each pattern is defined as a class attribute for easy access and modification.
    """
    OWNERSHIP_SECTION = r"własność(.*?)Działki ewidencyjne"
    COMPANY_OWNERSHIP_TYPE = r"własność\s*([A-Z\s]+)(?=\s*REGON)"
    COMPANY_OWNERSHIP_TYPE_NO_REGON = r"własność\s*([A-Z\s]+)"
    PRIVATE_OWNERSHIP_TYPE = r"własność\s*([A-ZĄĆĘŁŃÓŚŹŻ][a-zA-Z-ąćęłńóśźż]+(?:\s+[A-ZĄĆĘŁŃÓŚŹŻ][a-ząćęłńóśźż]+)+)"
    COMPANY_NAME = r"własność\s*([\s\S]+?)(?=\s*REGON)"
    COMPANY_ADDRESS = r"siedziba:\s*([\s\S]+?)(?=\s*Działki)"
    NOB = r"REGON:\s+(\d{9})"
    TIN = r"NIP:\s+(\d{10})"
    LAND_REGISTER = r"([A-Z]{2}\d[A-Z]/\d{8}/\d)"
    PARCEL_NUMBER = r"Użytek i klasa bonitacyjnaNr KW lub inne dokumentyOznaczenie Pow. \[ha\]\s*([\s\S]+?)\n"
    PARCEL_NUMBER_ADDITIONAL = r"(\d+/\d+|\d+)"
    REGISTRATION_UNIT = r"Jednostka ewidencyjna:\s*([^\n]+)"
    REGISTRATION_UNIT_ADDITIONAL = r",\s*([A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż\s]+)"
    CIRCLE = r"Obręb ewidencyjny:\s*([^\n]+)"
    PAGE_INFO = r"Strona\s+(\d+)\s+z\s+(\d+)"
    PRIVATE_OWNERSHIP = (
        r"(?P<name>[A-ZĄĆĘŁŃÓŚŹŻ][a-ząćęłńóśźż]+\s+[A-ZĄĆĘŁŃÓŚŹŻ][a-ząćęłńóśźż]+(?:\s*\([^)]+\))?)"
        r"(?:\s*PESEL\s*:\s*(?P<ssn>[\d\s]+))?\s*(adres|stały pobyt)\s*:\s*(?P<address>[^\n]+)"
    )



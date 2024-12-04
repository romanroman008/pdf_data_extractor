class Investor:
    def __init__(self, name, address, type_of_work, name_of_work):
        self.__name = name
        self.__address = address
        self.__type_of_work = type_of_work
        self.__name_of_work = name_of_work

    def get_name(self):
        return self.__name

    def get_address(self):
        return self.__address

    def get_type_of_work(self):
        return self.__type_of_work

    def get_name_of_work(self):
        return self.__name_of_work
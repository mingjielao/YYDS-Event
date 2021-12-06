from abc import ABC

class AddressDataTransferObject():

    def __init__(self, street, city, state, zipcode):
        self.street = street
        self.city = city
        self.state = state
        self.zipcode = zipcode


class BaseAddressService(ABC):

    def __init__(self):
        pass

    @classmethod
    def do_lookup(cls, address_dto):
        pass
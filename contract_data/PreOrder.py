
from brownie import PreOrder as MyContract

from contract_data.ContractBase import ContractBase

class PreOrder(ContractBase):
    def __init__(self):

        self.__contract = MyContract[-1]
        self.address = self.__contract.address

    def __getattr__(self, item):
        return getattr(self.__contract, item)

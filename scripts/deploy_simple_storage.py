from brownie import (
    network,
    accounts,
    config,
    Contract,
    web3,
    SimpleStorage
)

def main():
    account = accounts[0]
    simple_storage_contract = SimpleStorage.deploy({"from": account})
    print(simple_storage_contract.number())

    simple_storage_contract.setNumber(888, {"from": account})
    print(simple_storage_contract.number())


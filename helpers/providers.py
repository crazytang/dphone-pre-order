from brownie import config
from web3 import Web3, HTTPProvider


def get_provider() -> Web3:
    return Web3(HTTPProvider(config['networks']['development']['rpc']))

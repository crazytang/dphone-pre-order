from brownie import accounts, web3, config

from helpers.utils import obj_to_json


class SignatureInfo:
    def __init__(self, data: tuple):
        self.signed_message = data[0]
        self.r = data[1]
        self.s = data[2]
        self.v = data[3]
        self.signature: bytes = data[4]

class MixAccount:
    """
    Because I don't know how to get the LocalAccount object from Accounts, so I have to use the alternative MixAccount class
    It's not perfect solution.
    """
    def __init__(self, private_key):
        self.__brownie_account = accounts.add(private_key)
        # self.__local_account = LocalAccount(self.__brownie_account.address, self.__brownie_account, private_key)
        self.__w3_account = web3.eth.account.from_key(private_key)

    def __str__(self):
        return self.__brownie_account.address

    def __getattr__(self, key):
        def not_find(*args, **kwargs):
            err_msg = f'function or property：{key} is not exists in MixAccount, parameter is {args}, {kwargs}'
            raise Exception(err_msg)

        if key.strip('__') != key:
            return not_find

        if key in dir(self.__brownie_account):
            return getattr(self.__brownie_account, key)
        elif key in dir(self.__w3_account):
            return getattr(self.__w3_account, key)

        return not_find

    def __iter__(self, key):
        if key in self.__brownie_account.__dir__:
            return True
        elif key in self.__w3_account.__dir__:
            return True

        return False

    @property
    def account(self):
        return self.__brownie_account

    @property
    def address(self):
        return self.__brownie_account.address

    def signHash(self, _hash) -> SignatureInfo:
        return SignatureInfo(self.__w3_account.signHash(_hash))

def get_admin_account() -> MixAccount:
    # return MixAccount('0x9b36efaf96d1a30ce48803139f9e6d816cd116536ff7a6a1f8373fc0029bbc7b')
    _account = MixAccount(config['wallets']['admin_from_key'])
    print('admin address', _account.address)
    return _account

def get_user1_account() -> MixAccount:
    _account = MixAccount(config['wallets']['user1_from_key'])
    print('user1 address', _account.address)
    return _account

def get_user2_account() -> MixAccount:
    _account = MixAccount(config['wallets']['user2_from_key'])
    print('user2 address', _account.address)
    return _account

def get_user3_account() -> MixAccount:
    _account = MixAccount(config['wallets']['user3_from_key'])
    print('user3 address', _account.address)
    return _account

def get_user4_account() -> MixAccount:
    _account = MixAccount(config['wallets']['user4_from_key'])
    print('user4 address', _account.address)
    return _account

def get_user5_account() -> MixAccount:
    _account = MixAccount(config['wallets']['user5_from_key'])
    print('user5 address', _account.address)
    return _account


def get_sigs_from_operators(_hash: str, operators: list[MixAccount]) -> list[bytes]:
    sigs = []
    for op in operators:
        sigs.append(op.signHash(_hash).signature)

    return sigs
        
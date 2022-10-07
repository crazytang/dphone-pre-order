import web3
from brownie import accounts
from brownie.network.account import LocalAccount, Accounts
from brownie.network.web3 import Web3
from eth_account.messages import encode_defunct
from web3 import eth

from helpers.local_accounts import get_admin_account


def test_account():
    acc = get_admin_account()
    print('acc.address', acc.address)
    assert acc.address in accounts

    assert acc.private_key is not None

    _hash = Web3.sha3(text='23423423').hex()
    print('_hash', _hash)
    message = encode_defunct(hexstr=_hash)
    sig = acc.sign_message(message)
    print('sig', sig)
    assert sig.signature is not None
    assert eth.Account.recover_message(message, signature=sig.signature) == acc.address

    # acc.abc('abc', '123')

    # print(dir(accounts[len(accounts) - 1]), type(accounts[len(accounts) - 1]))
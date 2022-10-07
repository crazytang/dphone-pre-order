import pytest
from brownie import Contract
from brownie.network.account import PublicKeyAccount
from brownie.network.transaction import TransactionReceipt
from brownie.network.web3 import web3

from helpers.local_accounts import *
from helpers.utils import get_contract_abi, bn_to_number


@pytest.fixture
def account() -> PublicKeyAccount:
    account = get_admin_account()
    return account


# def test_operator(contract):
#     operator_address = contract.operators(0)
#
#     assert operator_address == get_user1_account().address


def test_connection(account):
    print('account.address', account.address)
    print('account.balance()', bn_to_number(account.balance()))
    print('account.get_deployment_address()', account.get_deployment_address())
    print('web3.chain_id', web3.chain_id)
    print('web3.eth.block_number', web3.eth.block_number)
    print('account.nonce', account.nonce)

def test_transaction_receipt():
    tx_hash = '0x1d23be807e3a2017fd693487fb4d184ccb18825bc752c4a90b70fc54135acdfc'
    tx_receipt = TransactionReceipt(tx_hash)

    print('tx_receipt', tx_receipt.events['AddedSupportedToken'])
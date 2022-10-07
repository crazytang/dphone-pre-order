from brownie import ProxyAdmin

from brownie.network.contract import ProjectContract

from helpers.local_accounts import *


def main():

    account = get_admin_account()

    proxy_admin: ProjectContract = ProxyAdmin.deploy({"from": account})
    print('proxy_admin address', proxy_admin.address)
    print('txid', proxy_admin.tx.txid)
    # print('receipt', web3.eth.get_transaction_receipt(proxy_admin.tx.txid))

    assert account.address == proxy_admin.tx.sender



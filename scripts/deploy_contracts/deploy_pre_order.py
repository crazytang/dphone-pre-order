
from brownie import PreOrder, TransparentUpgradeableProxy, ProxyAdmin
from brownie.network.contract import ProjectContract, Contract

from helpers.local_accounts import get_admin_account, get_user1_account, get_user2_account
from helpers.utils import encode_function_data


def main(*args):

    is_upgrade = 'upgrade' in args  # need to deploy a new contract

    account = get_admin_account()

    pre_order: ProjectContract = PreOrder.deploy({"from": account})
    print('pre_order address', pre_order.address)
    print('txid', pre_order.tx.txid)
    # print('receipt', web3.eth.get_transaction_receipt(proxy_admin.tx.txid))

    assert account.address == pre_order.tx.sender

    proxy_admin = ProxyAdmin[-1]

    operators = [account.address, get_user1_account().address, get_user2_account().address]
    call_data = encode_function_data(pre_order.initialize, operators)
    # print('call_data', call_data)
    if not is_upgrade:
        transparent_upgradeable_proxy: ProjectContract = TransparentUpgradeableProxy.deploy(pre_order.address, proxy_admin.address, call_data, {"from": account})
        print('transparent_upgradeable_proxy has been deployed txid', transparent_upgradeable_proxy.tx.txid)
        assert account.address == transparent_upgradeable_proxy.tx.sender
    else:
        transparent_upgradeable_proxy = TransparentUpgradeableProxy[-1]
        tx = proxy_admin.upgrade(transparent_upgradeable_proxy.address, pre_order.address, {"from": account})
        print('transparent_upgradeable_proxy has been upgraded address', tx.txid)

    proxy = Contract.from_abi("PreOrder", transparent_upgradeable_proxy.address, PreOrder.abi)

    operators_in_proxy = proxy.getOperators()
    # print('operators_in_proxy', operators_in_proxy)

    assert len(operators) == len(operators_in_proxy) == proxy.operator_limited_num()
    assert operators[0] == account.address


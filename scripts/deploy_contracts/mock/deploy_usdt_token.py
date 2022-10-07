from brownie import USDTToken

from helpers.local_accounts import *
from helpers.utils import bn_to_number


def main():
    account = get_admin_account()
    usdt = USDTToken.deploy({"from": account})

    balance = bn_to_number(usdt.balanceOf(account.address))
    total_supply = bn_to_number(usdt.totalSupply())

    assert balance == total_supply
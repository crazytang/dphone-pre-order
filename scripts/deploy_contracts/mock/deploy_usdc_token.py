from brownie import USDCToken

from helpers.local_accounts import *
from helpers.utils import bn_to_number


def main():
    account = get_admin_account()
    usdc = USDCToken.deploy({"from": account})

    balance = bn_to_number(usdc.balanceOf(account.address))
    total_supply = bn_to_number(usdc.totalSupply())

    assert balance == total_supply
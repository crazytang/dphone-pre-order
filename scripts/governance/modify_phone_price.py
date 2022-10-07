from helpers.local_accounts import *
from helpers.local_contracts import *
from helpers.utils import number_to_bn
import web3


def main():
    pre_order = get_pre_order_contract()
    admin_account = get_admin_account()
    operator2 = get_user1_account()
    operator3 = get_user2_account()

    # setting ETH price
    eth_price = 0.023
    eth_price_bn = number_to_bn(eth_price)
    token_address = web3.constants.ADDRESS_ZERO

    _hash = pre_order.getModifyPhonePriceHash(token_address, eth_price_bn)
    sigs = get_sigs_from_operators(_hash, [admin_account, operator3, operator2])
    tx = pre_order.modifyPhonePrice(token_address, eth_price_bn, sigs, {"from": admin_account})
    print('pre_order.modifyPhonePrice() ETH tx', tx.txid)
    assert eth_price_bn == pre_order.phone_prices(token_address)

    usdt = get_mock_usdt_contract()
    usdc = get_mock_usdc_contract()

    # setting USDT price
    usdt_price = 29.99
    usdt_price_bn = number_to_bn(usdt_price)

    _hash = pre_order.getModifyPhonePriceHash(usdt.address, usdt_price_bn)
    sigs = get_sigs_from_operators(_hash, [admin_account, operator3, operator2])

    tx = pre_order.modifyPhonePrice(usdt.address, usdt_price_bn, sigs, {"from": admin_account})
    print('pre_order.modifyPhonePrice() USDT tx', tx.txid)
    assert usdt_price_bn == pre_order.phone_prices(usdt.address)

    # setting USDC price
    usdc_price = 29.98
    usdc_price_bn = number_to_bn(usdc_price)
    _hash = pre_order.getModifyPhonePriceHash(usdc.address, usdc_price_bn)
    sigs = get_sigs_from_operators(_hash, [admin_account, operator3, operator2])

    tx = pre_order.modifyPhonePrice(usdc.address, usdc_price_bn, sigs, {"from": admin_account})
    print('pre_order.modifyPhonePrice() USDC tx', tx.txid)
    assert usdc_price_bn == pre_order.phone_prices(usdc.address)

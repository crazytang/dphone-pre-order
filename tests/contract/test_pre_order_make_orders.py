import brownie
import pytest
import web3

from helpers.local_contracts import *
from helpers.utils import bn_to_number, number_to_bn, amount_equal_in_precision


def test_base(pre_order, admin_operator, operator1, operator2):
    operators_in_contract = pre_order.getOperators()
    operators_num = pre_order.operator_limited_num()
    assert len(operators_in_contract) == operators_num
    assert admin_operator.address in operators_in_contract
    assert operator1.address in operators_in_contract
    assert operator2.address in operators_in_contract

    assert pre_order.isOperator(admin_operator.address)

    # 0x0 means ETH
    assert pre_order.isSupportedToken(web3.constants.ADDRESS_ZERO)

    usdt = get_mock_usdt_contract()
    is_supported_token = pre_order.isSupportedToken(usdt.address)
    print('USDT supported is %s' % is_supported_token)

    usdc = get_mock_usdc_contract()
    is_supported_token = pre_order.isSupportedToken(usdc.address)
    print('USDC supported is %s' % is_supported_token)

    asset_recipient_address = pre_order.asset_recipient()
    print('asset_recipient has been point to %s' % asset_recipient_address)

    users = pre_order.getUsers()
    print('users', users)

def test_make_pre_order_direct_send_eth(pre_order, operator3, provider):
    # pytest.skip('skipping')
    user_account = operator3
    user_eth_old_balance = bn_to_number(provider.eth.get_balance(user_account.address))
    print('user_eth_old_balance', user_eth_old_balance)

    contract_eth_old_balance = bn_to_number(provider.eth.get_balance(pre_order.address))
    print('contract_eth_old_balance', contract_eth_old_balance)

    user_old_order_num = pre_order.users_pre_order_num(user_account.address)
    print('user_old_order_num', user_old_order_num)

    user_old_deposited_amount = bn_to_number(pre_order.users_deposit(user_account.address, web3.constants.ADDRESS_ZERO))
    print('user_old_deposited_amount', user_old_deposited_amount)

    pre_order_num = 3
    phone_eth_price = bn_to_number(pre_order.phone_prices(web3.constants.ADDRESS_ZERO))
    print('phone_eth_price', phone_eth_price)
    assert phone_eth_price > 0

    eth_amount = pre_order_num * phone_eth_price
    print('eth_amount', eth_amount)

    tx = user_account.account.transfer(pre_order.address, number_to_bn(eth_amount))
    print('user has transfer %s eth to pre_order contract. tx', tx.txid)
    tx.wait(2)

    # print('tx', tx.__dict__)

    gas_fee = bn_to_number(tx.gas_used * tx.gas_price)
    print('gas_fee', gas_fee)
    user_eth_new_balance = bn_to_number(provider.eth.get_balance(user_account.address))
    print('user_eth_new_balance', user_eth_new_balance)
    assert amount_equal_in_precision(user_eth_new_balance, user_eth_old_balance - eth_amount - gas_fee)

    contract_eth_new_balance = bn_to_number(provider.eth.get_balance(pre_order.address))
    print('contract_eth_new_balance', contract_eth_new_balance)
    assert amount_equal_in_precision(contract_eth_new_balance, contract_eth_old_balance + eth_amount)

    user_new_order_num = pre_order.users_pre_order_num(user_account.address)
    print('user_new_order_num', user_new_order_num)
    assert user_new_order_num == user_old_order_num + pre_order_num

    user_new_deposited_amount = bn_to_number(pre_order.users_deposit(user_account.address, web3.constants.ADDRESS_ZERO))
    print('user_new_deposited_amount', user_new_deposited_amount)
    assert amount_equal_in_precision(user_new_deposited_amount, user_old_deposited_amount + eth_amount)


def test_make_pre_order_using_eth(pre_order, operator3, provider):
    # pytest.skip('skipping')
    user_account = operator3
    user_eth_old_balance = bn_to_number(provider.eth.get_balance(user_account.address))
    print('user_eth_old_balance', user_eth_old_balance)

    contract_eth_old_balance = bn_to_number(provider.eth.get_balance(pre_order.address))
    print('contract_eth_old_balance', contract_eth_old_balance)

    user_old_order_num = pre_order.users_pre_order_num(user_account.address)
    print('user_old_order_num', user_old_order_num)

    user_old_deposited_amount = bn_to_number(pre_order.users_deposit(user_account.address, web3.constants.ADDRESS_ZERO))
    print('user_old_deposited_amount', user_old_deposited_amount)

    pre_order_num = 4
    phone_eth_price = bn_to_number(pre_order.phone_prices(web3.constants.ADDRESS_ZERO))
    print('phone_eth_price', phone_eth_price)
    assert phone_eth_price > 0

    eth_amount = pre_order_num * phone_eth_price
    print('eth_amount', eth_amount)

    tx = pre_order.makePreOrderUsingETH({"from": user_account, "value": number_to_bn(eth_amount), "allow_revert": True, "gas_limit": 30000000})
    print('pre_order.makePreOrderUsingETH() tx', tx.txid)
    tx.wait(2)

    gas_fee = bn_to_number(tx.gas_used * tx.gas_price)
    print('gas_fee', gas_fee)
    user_eth_new_balance = bn_to_number(provider.eth.get_balance(user_account.address))
    print('user_eth_new_balance', user_eth_new_balance)
    assert amount_equal_in_precision(user_eth_new_balance, user_eth_old_balance - eth_amount - gas_fee)

    contract_eth_new_balance = bn_to_number(provider.eth.get_balance(pre_order.address))
    print('contract_eth_new_balance', contract_eth_new_balance)
    assert amount_equal_in_precision(contract_eth_new_balance, contract_eth_old_balance + eth_amount)

    user_new_order_num = pre_order.users_pre_order_num(user_account.address)
    print('user_new_order_num', user_new_order_num)
    assert user_new_order_num == user_old_order_num + pre_order_num

    user_new_deposited_amount = bn_to_number(pre_order.users_deposit(user_account.address, web3.constants.ADDRESS_ZERO))
    print('user_new_deposited_amount', user_new_deposited_amount)
    assert amount_equal_in_precision(user_new_deposited_amount, user_old_deposited_amount + eth_amount)


def test_make_pre_order_using_usdt(pre_order, admin_operator, mock_usdt):
    # pytest.skip('skipping')
    user_account = admin_operator
    user_usdt_old_balance = bn_to_number(mock_usdt.balanceOf(user_account.address))
    print('user_usdt_old_balance', user_usdt_old_balance)

    contract_usdt_old_balance = bn_to_number(mock_usdt.balanceOf(pre_order.address))
    print('contract_usdt_old_balance', contract_usdt_old_balance)

    user_old_order_num = pre_order.users_pre_order_num(user_account.address)
    print('user_old_order_num', user_old_order_num)

    user_old_deposited_amount = bn_to_number(pre_order.users_deposit(user_account.address, mock_usdt.address))
    print('user_old_deposited_amount', user_old_deposited_amount)

    pre_order_num = 4
    phone_usdt_price = bn_to_number(pre_order.phone_prices(mock_usdt.address))
    print('phone_usdt_price', phone_usdt_price)
    assert phone_usdt_price > 0

    usdt_amount = pre_order_num * phone_usdt_price
    print('usdt_amount', usdt_amount)

    if mock_usdt.allowance(user_account.address, pre_order.address) <= number_to_bn(usdt_amount):
        tx = mock_usdt.approve(pre_order.address, web3.constants.MAX_INT, {"from": user_account})
        print('mock_usdt.approve() tx', tx.txid)
        tx.wait(1)

    tx = pre_order.makePreOrderUsingToken(mock_usdt.address, number_to_bn(usdt_amount), {"from": user_account})
    print('pre_order.makePreOrderUsingToken() tx', tx.txid)
    tx.wait(2)

    user_usdt_new_balance = bn_to_number(mock_usdt.balanceOf(user_account.address))
    print('user_usdt_new_balance', user_usdt_new_balance)
    assert amount_equal_in_precision(user_usdt_new_balance, user_usdt_old_balance - usdt_amount)

    contract_usdt_new_balance = bn_to_number(mock_usdt.balanceOf(pre_order.address))
    print('contract_usdt_new_balance', contract_usdt_new_balance)
    assert amount_equal_in_precision(contract_usdt_new_balance, contract_usdt_old_balance + usdt_amount)

    user_new_order_num = pre_order.users_pre_order_num(user_account.address)
    print('user_new_order_num', user_new_order_num)
    assert user_new_order_num == user_old_order_num + pre_order_num

    user_new_deposited_amount = bn_to_number(pre_order.users_deposit(user_account.address, mock_usdt.address))
    print('user_new_deposited_amount', user_new_deposited_amount)
    assert amount_equal_in_precision(user_new_deposited_amount, user_old_deposited_amount + usdt_amount)


def test_make_pre_order_using_usdc(pre_order, admin_operator, mock_usdc):
    # pytest.skip('skipping')
    user_account = admin_operator
    user_usdc_old_balance = bn_to_number(mock_usdc.balanceOf(user_account.address))
    print('user_usdc_old_balance', user_usdc_old_balance)

    contract_usdc_old_balance = bn_to_number(mock_usdc.balanceOf(pre_order.address))
    print('contract_usdc_old_balance', contract_usdc_old_balance)

    user_old_order_num = pre_order.users_pre_order_num(user_account.address)
    print('user_old_order_num', user_old_order_num)

    user_old_deposited_amount = bn_to_number(pre_order.users_deposit(user_account.address, mock_usdc.address))
    print('user_old_deposited_amount', user_old_deposited_amount)

    pre_order_num = 4
    phone_usdc_price = bn_to_number(pre_order.phone_prices(mock_usdc.address))
    print('phone_usdc_price', phone_usdc_price)
    assert phone_usdc_price > 0

    usdc_amount = pre_order_num * phone_usdc_price
    print('usdc_amount', usdc_amount)

    if mock_usdc.allowance(user_account.address, pre_order.address) <= number_to_bn(usdc_amount):
        tx = mock_usdc.approve(pre_order.address, web3.constants.MAX_INT, {"from": user_account})
        print('mock_usdc.approve() tx', tx.txid)
        tx.wait(1)

    tx = pre_order.makePreOrderUsingToken(mock_usdc.address, number_to_bn(usdc_amount), {"from": user_account})
    print('pre_order.makePreOrderUsingToken() tx', tx.txid)
    tx.wait(2)

    user_usdc_new_balance = bn_to_number(mock_usdc.balanceOf(user_account.address))
    print('user_usdc_new_balance', user_usdc_new_balance)
    assert amount_equal_in_precision(user_usdc_new_balance, user_usdc_old_balance - usdc_amount)

    contract_usdc_new_balance = bn_to_number(mock_usdc.balanceOf(pre_order.address))
    print('contract_usdc_new_balance', contract_usdc_new_balance)
    assert amount_equal_in_precision(contract_usdc_new_balance, contract_usdc_old_balance + usdc_amount)

    user_new_order_num = pre_order.users_pre_order_num(user_account.address)
    print('user_new_order_num', user_new_order_num)
    assert user_new_order_num == user_old_order_num + pre_order_num

    user_new_deposited_amount = bn_to_number(pre_order.users_deposit(user_account.address, mock_usdc.address))
    print('user_new_deposited_amount', user_new_deposited_amount)
    assert amount_equal_in_precision(user_new_deposited_amount, user_old_deposited_amount + usdc_amount)


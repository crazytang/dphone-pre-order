import pytest
import web3
from brownie import Contract

from helpers.local_accounts import get_sigs_from_operators
from helpers.utils import bn_to_number, amount_equal_in_precision


def test_pre_order_fail(pre_order, mock_usdt, mock_usdc, provider, admin_operator, operator1, operator2, operator5):
    pytest.skip('skip')
    users = pre_order.getUsers()
    print('users', users)


    supported_tokens = pre_order.getAllSupportedTokens()
    print('supported_tokens', supported_tokens)
    tokens: list[Contract] = []
    for token_address in supported_tokens:
        if token_address == mock_usdt.address:
            tokens.append(mock_usdt)
        elif token_address == mock_usdc.address:
            tokens.append(mock_usdc)

    print('tokens', tokens)

    users_old_eth_balance = dict()
    users_old_eth_balance_in_contract = dict()
    users_old_tokens_balance = dict()
    users_old_tokens_balance_in_contract = dict()

    for user_address in users:
        users_old_eth_balance[user_address] = bn_to_number(provider.eth.get_balance(user_address))
        users_old_eth_balance_in_contract[user_address] = \
            bn_to_number(pre_order.users_deposit(user_address, web3.constants.ADDRESS_ZERO))

        for token_contract in tokens:
            if user_address not in users_old_tokens_balance:
                users_old_tokens_balance[user_address] = dict()
                users_old_tokens_balance_in_contract[user_address] = dict()

            users_old_tokens_balance[user_address][token_contract.address] = bn_to_number(token_contract.balanceOf(user_address))
            users_old_tokens_balance_in_contract[user_address][token_contract.address] = \
                bn_to_number(pre_order.users_deposit(user_address, token_contract.address))

    print('users_old_eth_balance', users_old_eth_balance)
    print('users_old_eth_balance_in_contract', users_old_eth_balance_in_contract)
    print('users_old_tokens_balance', users_old_tokens_balance)
    print('users_old_tokens_balance_in_contract', users_old_tokens_balance_in_contract)

    _hash = pre_order.getPreOrderFailHash()
    sigs = get_sigs_from_operators(_hash, [admin_operator, operator1, operator2])

    tx = pre_order.preOrderFail(sigs, {"from": operator5})
    print('pre_order.preOrderFail() tx', tx.txid)
    tx.wait(2)

    assert provider.eth.get_balance(pre_order.address) == 0
    assert mock_usdc.balanceOf(pre_order.address) == 0
    assert mock_usdt.balanceOf(pre_order.address) == 0

    users_new_eth_balance = dict()
    users_new_eth_balance_in_contract = dict()
    users_new_tokens_balance = dict()
    users_new_tokens_balance_in_contract = dict()

    for user_address in users:
        users_new_eth_balance[user_address] = bn_to_number(provider.eth.get_balance(user_address))
        assert amount_equal_in_precision(users_new_eth_balance[user_address], \
               users_old_eth_balance[user_address] + users_old_eth_balance_in_contract[user_address])

        users_new_eth_balance_in_contract[user_address] = bn_to_number(pre_order.users_deposit(user_address, web3.constants.ADDRESS_ZERO))
        assert users_new_eth_balance_in_contract[user_address] == 0

        for token_contract in tokens:
            if user_address not in users_new_tokens_balance:
                users_new_tokens_balance[user_address] = dict()
                users_new_tokens_balance_in_contract[user_address] = dict()
            users_new_tokens_balance_in_contract[user_address][token_contract.address] = \
                bn_to_number(pre_order.users_deposit(user_address, token_contract.address))
            users_new_tokens_balance[user_address][token_contract.address] = bn_to_number(token_contract.balanceOf(user_address))
            assert users_new_tokens_balance_in_contract[user_address][token_contract.address] == 0

            assert amount_equal_in_precision(users_new_tokens_balance[user_address][token_contract.address], \
                   users_old_tokens_balance[user_address][token_contract.address] + \
                   users_old_tokens_balance_in_contract[user_address][token_contract.address])


    print('users_new_eth_balance', users_new_eth_balance)
    print('users_new_eth_balance_in_contract', users_new_eth_balance_in_contract)
    print('users_new_tokens_balance', users_new_tokens_balance)
    print('users_new_tokens_balance_in_contract', users_new_tokens_balance_in_contract)


def test_pre_order_succ(pre_order, mock_usdt, mock_usdc, provider, admin_operator, operator1, operator2, operator5):
    recipient_address = pre_order.asset_recipient()
    print('recipient_address', recipient_address)

    recipient_old_eth_balance = bn_to_number(provider.eth.get_balance(recipient_address))
    print('recipient_old_eth_balance', recipient_old_eth_balance)

    recipient_old_eth_balance_in_contract = bn_to_number(provider.eth.get_balance(pre_order.address))
    print('recipient_old_eth_balance_in_contract', recipient_old_eth_balance_in_contract)

    recipient_old_usdt_balance = bn_to_number(mock_usdt.balanceOf(recipient_address))
    print('recipient_old_usdt_balance', recipient_old_usdt_balance)

    recipient_old_usdt_balance_in_contract = bn_to_number(mock_usdt.balanceOf(pre_order.address))
    print('recipient_old_usdt_balance_in_contract', recipient_old_usdt_balance_in_contract)

    recipient_old_usdc_balance = bn_to_number(mock_usdc.balanceOf(recipient_address))
    print('recipient_old_usdc_balance', recipient_old_usdc_balance)

    recipient_old_usdc_balance_in_contract = bn_to_number(mock_usdc.balanceOf(pre_order.address))
    print('recipient_old_usdc_balance_in_contract', recipient_old_usdc_balance_in_contract)

    _hash = pre_order.getPreOrderSucc()
    sigs = get_sigs_from_operators(_hash, [admin_operator, operator1, operator2])

    tx = pre_order.preOrderSucc(sigs, {"from": operator5, "allow_revert": True, "gas_limit": 30000000})
    print('pre_order.preOrderSucc() tx', tx.txid)
    tx.wait(2)

    recipient_new_eth_balance = bn_to_number(provider.eth.get_balance(recipient_address))
    print('recipient_new_eth_balance', recipient_new_eth_balance)
    assert amount_equal_in_precision(recipient_new_eth_balance, recipient_old_eth_balance + recipient_old_eth_balance_in_contract)
    assert provider.eth.get_balance(pre_order.address) == 0

    recipient_new_usdt_balance = bn_to_number(mock_usdt.balanceOf(recipient_address))
    print('recipient_new_usdt_balance', recipient_new_usdt_balance)
    assert amount_equal_in_precision(recipient_new_usdt_balance, recipient_old_usdt_balance + recipient_old_usdt_balance_in_contract)
    assert mock_usdt.balanceOf(pre_order.address) == 0

    recipient_new_usdc_balance = bn_to_number(mock_usdc.balanceOf(recipient_address))
    print('recipient_new_usdc_balance', recipient_new_usdc_balance)
    assert amount_equal_in_precision(recipient_new_usdc_balance, recipient_old_usdc_balance + recipient_old_usdc_balance_in_contract)
    assert mock_usdc.balanceOf(pre_order.address) == 0

import datetime

import pytest
from brownie.network.transaction import TransactionReceipt

from helpers.local_contracts import *
from helpers.local_accounts import *


def test_multi_sig():
    pytest.skip('skipping')
    pre_order = get_pre_order_contract()

    operators = pre_order.getOperators()
    print('operators', operators)

    operator1 = get_admin_account()
    assert operator1.address == operators[0]

    operator2 = get_user1_account()
    assert operator2 == operators[1]

    operator3 = get_user2_account()
    assert operator3 == operators[2]

    operator5 = get_user5_account()

    usdc = get_mock_usdc_contract()

    _hash = pre_order.getAddSupportedTokenHash(usdc.address)
    print('_hash', _hash)

    op1_sig = operator1.signHash(_hash).signature
    # print('op1_sig', op1_sig)
    op2_sig = operator2.signHash(_hash).signature
    # print('op2_sig', op2_sig)
    op3_sig = operator3.signHash(_hash).signature
    # print('op3_sig', op3_sig)

    # sigs = [op1_sig, op2_sig, op3_sig]
    sigs = [op2_sig, op3_sig, op1_sig]

    is_supported_token: bool = pre_order.isSupportedToken(usdc.address)
    print('is_supported_token', is_supported_token)

    if not is_supported_token:
        tx: TransactionReceipt = pre_order.addSupportedToken(usdc.address, sigs, {"from": operator5, "allow_revert": True})
        print('pre_order.addSupportedToken() tx', tx.txid)
    else:
        print('the %s token had been added' % usdc.address)

    op5_sig = operator5.signHash(_hash).signature

    try:
        # operators is less than 3
        sigs = [op2_sig, op3_sig]
        tx = pre_order.addSupportedToken(usdc.address, sigs, {"from": operator5, "allow_revert": True})
    except Exception as e:
        # print('revert error:', format(e))
        assert str(e).find('PreOrder: Only operators can addSupportedToken') > -1

    try:
        # one of operator is no be granted
        sigs = [op2_sig, op3_sig, op5_sig]
        tx = pre_order.addSupportedToken(usdc.address, sigs, {"from": operator5, "allow_revert": True})
    except Exception as e:
        # print('revert error:', format(e))
        assert str(e).find('PreOrder: Only operators can addSupportedToken') > -1


def test_sign_and_verifty(admin_operator, provider):
    account = admin_operator
    message = str(int(datetime.datetime.now().timestamp()))
    print('message', message)
    # message = encode_defunct(hexstr=str(_hash))
    # sig = provider.eth.account.sign_message(message, account1.privateKey)
    # print('type(account)', type(account))
    _hash = provider.sha3(text=message)
    print('_hash', _hash)
    sig = account.signHash(_hash)
    # sig = provider.eth.account.signHash(_hash, account1.privateKey)
    print('sig', sig)
    # recover_address = provider.eth.account.recover_message(message, signature=sig.signature)
    recover_address = provider.eth.account.recoverHash(_hash, signature=sig.signature)
    print('verify', recover_address)
    assert recover_address == account.address
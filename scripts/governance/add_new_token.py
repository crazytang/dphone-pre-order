from helpers.local_accounts import *
from helpers.local_contracts import *

def main():
    pre_order = get_pre_order_contract()
    new_token = get_mock_usdt_contract()

    admin_account = get_admin_account()
    operator2 = get_user1_account()
    operator3 = get_user2_account()

    if not pre_order.isSupportedToken(new_token.address):
        _hash = pre_order.getAddSupportedTokenHash(new_token.address)

        sigs = get_sigs_from_operators(_hash, [admin_account, operator3, operator2])

        tx = pre_order.addSupportedToken(new_token.address, sigs, {"from": admin_account})
        print('pre_order.addSupportedToken() tx', tx.txid)
    else:
        print('This token %s had been added' % new_token.address)

    new_token = get_mock_usdc_contract()
    if not pre_order.isSupportedToken(new_token.address):
        _hash = pre_order.getAddSupportedTokenHash(new_token.address)

        sigs = get_sigs_from_operators(_hash, [admin_account, operator3, operator2])

        tx = pre_order.addSupportedToken(new_token.address, sigs, {"from": admin_account})
        print('pre_order.addSupportedToken() tx', tx.txid)
    else:
        print('This token %s had been added' % new_token.address)
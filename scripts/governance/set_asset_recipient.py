from helpers.local_accounts import *
from helpers.local_contracts import get_pre_order_contract


def main():
    pre_order = get_pre_order_contract()

    admin_account = get_admin_account()
    operator2 = get_user1_account()
    operator3 = get_user2_account()

    recipient_address = admin_account.address

    _hash = pre_order.getSetRecipientHash(recipient_address)
    sigs = get_sigs_from_operators(_hash, [admin_account, operator3, operator2])

    tx = pre_order.setRecipient(recipient_address, sigs, {"from":admin_account})
    print('pre_order.setRecipient() tx', tx.txid)

    assert recipient_address == pre_order.asset_recipient()
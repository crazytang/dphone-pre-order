#! /bin/bash

# deploy ProxyAdmin
brownie run scripts/deploy_contracts/deploy_proxy_admin.py main --network goerli-fork
# deploy fully new contract
brownie run scripts/deploy_contracts/deploy_pre_order.py main --network goerli-fork

# deploy mock tokens
brownie run scripts/deploy_contracts/mock/deploy_usdc_token.py main --network goerli-fork
brownie run scripts/deploy_contracts/mock/deploy_usdt_token.py main --network goerli-fork

# upgrade contract
#brownie run scripts/deploy_contracts/deploy_pre_order.py main upgrade --network goerli-fork

# governance
brownie run scripts/governance/add_new_token.py --network goerli-fork
brownie run scripts/governance/modify_phone_price.py --network goerli-fork
brownie run scripts/governance/set_asset_recipient.py --network goerli-fork

# testing
brownie test tests/contract/test_pre_order_make_orders.py --disable-warnings --network goerli-fork -s

# end the pre order
brownie test tests/contract/test_pre_order_finish.py --disable-warnings --network goerli-fork -s

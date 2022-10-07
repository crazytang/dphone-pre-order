from brownie import PreOrder, TransparentUpgradeableProxy, USDCToken, USDTToken, Contract

def get_mock_usdc_contract() -> Contract:
    usdc = USDCToken[-1]
    print('Using USDCToken', usdc.address)
    return usdc

def get_mock_usdt_contract() -> Contract:
    usdt = USDTToken[-1]
    print('Using USDTToken', usdt.address)
    return usdt

def get_pre_order_contract() -> Contract:
    transparent_upgradeable_proxy = TransparentUpgradeableProxy[-1]
    proxy = Contract.from_abi("PreOrder", transparent_upgradeable_proxy.address, PreOrder.abi)
    print('Using PreOrder Proxy', proxy.address)
    return proxy


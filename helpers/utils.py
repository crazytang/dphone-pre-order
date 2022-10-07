import json
import os.path
from typing import Union

import web3


def get_contract_abi(contract_address, chain_id):
    _path = os.path.abspath('build/deployments/%s/%s.json' %(chain_id, contract_address))
    with open(_path, 'rb') as f:
        data = json.loads(f.read())
        return data['abi']

def bn_to_number(big_number: int) -> float:
    return float(web3.Web3.fromWei(big_number, 'ether'))

def number_to_bn(number: Union[int,float]) -> int:
    return web3.Web3.toWei(number, 'ether')

def compare_number_precision() -> float:
    return 0.000001

def amount_equal_in_precision(amount1: float, amount2: float, precision=compare_number_precision()) -> bool:
    gap = abs(amount1 - amount2)
    return gap < precision


def encode_function_data(initializer=None, *args):
    """Encodes the function call so we can work with an initializer.

    Args:
        initializer ([brownie.network.contract.ContractTx], optional):
        The initializer function we want to call. Example: `box.store`.
        Defaults to None.

        args (Any, optional):
        The arguments to pass to the initializer function

    Returns:
        [bytes]: Return the encoded bytes.
    """
    if not len(args): args = b''

    if initializer: return initializer.encode_input(*args)

    return b''

def obj_to_json(obj: object):
    return json.dumps(obj, default=lambda obj: obj.__dict__)
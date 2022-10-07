import pytest

from helpers.local_accounts import *
from helpers.local_contracts import *
from helpers.providers import get_provider


@pytest.fixture
def admin_operator() -> MixAccount:
    return get_admin_account()

@pytest.fixture
def operator1() -> MixAccount:
    return get_user1_account()

@pytest.fixture
def operator2() -> MixAccount:
    return get_user2_account()

@pytest.fixture
def operator3() -> MixAccount:
    return get_user3_account()

@pytest.fixture
def operator4() -> MixAccount:
    return get_user4_account()

@pytest.fixture
def operator5() -> MixAccount:
    return get_user5_account()

@pytest.fixture
def correct_sigs(_hash, admin_operator, operator1, operator2):
    return get_sigs_from_operators(_hash, [admin_operator, operator1, operator2])

@pytest.fixture
def provider():
    return get_provider()

@pytest.fixture
def pre_order():
    return get_pre_order_contract()

@pytest.fixture
def mock_usdt():
    return get_mock_usdt_contract()

@pytest.fixture
def mock_usdc():
    return get_mock_usdc_contract()
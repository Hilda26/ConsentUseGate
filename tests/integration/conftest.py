import os

import pytest
from gltest import get_contract_factory

CONTRACT_PATH = "consent_use_gate.py"


def _address_from_env() -> str | None:
    return os.environ.get("CONSENTUSEGATE_ADDRESS")


@pytest.fixture(scope="session")
def deployed_contract():
    address = _address_from_env()
    if not address:
        pytest.skip(
            "CONSENTUSEGATE_ADDRESS not set - deploy first with "
            "`genlayer deploy --contract contracts/consent_use_gate.py` "
            "and export the printed address."
        )
    factory = get_contract_factory(contract_file_path=CONTRACT_PATH)
    return factory.build_contract(contract_address=address)

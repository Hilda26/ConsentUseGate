import pytest

pytestmark = pytest.mark.integration


def test_deployed_schema_exposes_consent_use_gate_surface(deployed_contract):
    assert int(deployed_contract.policy_count(args=[]).call()) >= 0
    assert int(deployed_contract.request_count_total(args=[]).call()) >= 0

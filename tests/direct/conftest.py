import atexit
import os
import sys

import pytest


def _tolerant_unlink(path, *args, **kwargs):
    try:
        return _real_unlink(path, *args, **kwargs)
    except PermissionError:
        _leaked_files.append(path)


_leaked_files = []
_real_unlink = os.unlink

if sys.platform == "win32":
    os.unlink = _tolerant_unlink

    def _sweep_leaked_files():
        for path in _leaked_files:
            try:
                os.remove(path)
            except OSError:
                pass

    atexit.register(_sweep_leaked_files)


def _addr_bytes(addr) -> bytes:
    if isinstance(addr, bytes):
        return addr
    return bytes(addr.as_bytes)


def _install_transfer_hook(vm) -> None:
    def _hook(vm, request):
        if not isinstance(request, dict):
            return None
        msg = request.get("PostMessage") or request.get("EthSend")
        if msg is None:
            return None
        target = _addr_bytes(msg["address"])
        value = int(msg["value"])
        contract_addr = vm._contract_address
        contract_bytes = contract_addr if isinstance(contract_addr, bytes) else bytes(contract_addr)
        vm._balances[contract_bytes] = vm._balances.get(contract_bytes, 0) - value
        vm._balances[target] = vm._balances.get(target, 0) + value
        return {"ok": None}

    vm._gl_call_hook = _hook


@pytest.fixture
def direct_vm_with_transfers(direct_vm):
    _install_transfer_hook(direct_vm)
    return direct_vm


def warp_to(direct_vm, iso: str) -> None:
    direct_vm.warp(iso)


@pytest.fixture(autouse=True)
def _reset_known_contract():
    yield
    try:
        import genlayer.gl.genvm_contracts as gc

        gc.__known_contract__ = None
    except ImportError:
        pass

from pathlib import Path

import pytest

from ..conftest import configure_csr, csr, unconfigure_csr


@pytest.fixture(scope="session")
def csr01():
    csr01 = csr("csr01")
    csr01.connect()
    yield csr01
    csr01.disconnect()


@pytest.fixture
def configured_csr01(csr01):
    configure_csr(csr01, Path(__file__).parent / "csr01_config.txt")
    yield csr01
    unconfigure_csr(csr01)

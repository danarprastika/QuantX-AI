"""Pytest configuration for worker tests."""

import pytest


@pytest.fixture
def anyio_backend():
    return "asyncio"

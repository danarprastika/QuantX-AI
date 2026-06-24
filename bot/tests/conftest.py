"""Pytest configuration for bot tests."""

import pytest


@pytest.fixture
def anyio_backend():
    return "asyncio"

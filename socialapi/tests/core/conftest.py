# Override the async db fixture from parent conftest.py
# This allows sync tests in this directory to run without the database setup
import pytest


@pytest.fixture(autouse=True)
def db():
    """No-op fixture that overrides the async db fixture for sync tests."""
    yield

"""
conftest.py — Pytest fixtures shared across all tests.
"""

import pytest
from core.api_client import APIClient
from core.config_loader import load_config
from utils.logger import setup_logger

logger = setup_logger("api_tests")


@pytest.fixture(scope="session")
def config():
    """Load environment config once per test session."""
    return load_config()


@pytest.fixture(scope="session")
def api_client(config):
    """Authenticated APIClient shared across the session."""
    client = APIClient(
        base_url=config["base_url"],
        auth_type=config.get("auth_type"),
        token=config.get("token"),
        api_key=config.get("api_key"),
        timeout=config.get("timeout", 30),
        retries=config.get("retries", 3),
    )
    yield client
    client.close()


@pytest.fixture(scope="function")
def fresh_client(config):
    """A fresh client for tests that need isolation."""
    client = APIClient(
        base_url=config["base_url"],
        auth_type=config.get("auth_type"),
        token=config.get("token"),
        api_key=config.get("api_key"),
    )
    yield client
    client.close()


def pytest_configure(config):
    config.addinivalue_line("markers", "smoke: quick sanity checks")
    config.addinivalue_line("markers", "regression: full regression suite")
    config.addinivalue_line("markers", "performance: response-time assertions")
    config.addinivalue_line("markers", "auth: authentication-related tests")


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    passed = len(terminalreporter.stats.get("passed", []))
    failed = len(terminalreporter.stats.get("failed", []))
    logger.info(f"Test run complete — ✅ {passed} passed | ❌ {failed} failed")

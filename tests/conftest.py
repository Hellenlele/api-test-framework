import pytest
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from framework.base_test import BaseAPITest


def pytest_configure(config):
    os.makedirs('reports', exist_ok=True)


def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="demo",
        help="Environment to run tests against (demo, local, dev, staging, prod)"
    )


@pytest.fixture(scope="session")
def environment_name(request):
    return request.config.getoption("--env")
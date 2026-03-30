import pytest
import json
import os
import logging
from typing import Dict, Any
from .api_client import APIClient
from .assertions import APIAssertions
from .config_manager import ConfigManager


class BaseAPITest:
    @pytest.fixture(scope="session", autouse=True)
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('reports/test_execution.log'),
                logging.StreamHandler()
            ]
        )
    
    @pytest.fixture(scope="session")
    def config(self):
        return ConfigManager()
    
    @pytest.fixture(scope="session")
    def environment(self, config):
        env_name = os.getenv('TEST_ENV', 'demo')
        return config.get_environment_config(env_name)
    
    @pytest.fixture(scope="session")
    def api_client(self, environment, config):
        client = APIClient(
            base_url=environment['base_url'],
            timeout=environment.get('timeout', 30)
        )
        
        # Set up authentication
        auth_config = environment.get('auth', {})
        if auth_config.get('type') == 'bearer':
            client.set_auth('bearer', token=auth_config.get('token'))
        elif auth_config.get('type') == 'api_key':
            client.set_auth('api_key',
                          key_name=auth_config.get('key_name', 'X-API-Key'),
                          api_key=auth_config.get('api_key'))
        elif auth_config.get('type') == 'basic':
            client.set_auth('basic', 
                          username=auth_config.get('username'),
                          password=auth_config.get('password'))
        
        # Set default headers
        default_headers = config.get_default_headers()
        if default_headers:
            client.set_headers(default_headers)
        
        return client
    
    @pytest.fixture(scope="session")
    def test_data(self):
        data_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'test_data.json')
        with open(data_file, 'r') as f:
            return json.load(f)
    
    @pytest.fixture
    def assert_api(self):
        return APIAssertions()
    
    def log_test_info(self, test_name: str, endpoint: str, method: str):
        logging.info(f"Starting test: {test_name} - {method} {endpoint}")
    
    def log_test_result(self, test_name: str, passed: bool, message: str = ""):
        status = "PASSED" if passed else "FAILED"
        logging.info(f"Test result: {test_name} - {status} {message}")
    
    @staticmethod
    def validate_response_schema(response, schema: Dict[str, Any]):
        APIAssertions.assert_json_schema(response, schema)
    
    @staticmethod
    def assert_response_time(response, max_time_ms: int = 5000):
        APIAssertions.assert_response_time(response, max_time_ms)
import json
import jsonschema
from typing import Dict, Any, List, Union
import requests


class APIAssertions:
    @staticmethod
    def assert_status_code(response: requests.Response, expected_status: int):
        actual_status = response.status_code
        assert actual_status == expected_status, \
            f"Expected status code {expected_status}, but got {actual_status}. Response: {response.text[:200]}"
    
    @staticmethod
    def assert_status_code_in(response: requests.Response, expected_statuses: List[int]):
        actual_status = response.status_code
        assert actual_status in expected_statuses, \
            f"Expected status code to be one of {expected_statuses}, but got {actual_status}. Response: {response.text[:200]}"
    
    @staticmethod
    def assert_response_time(response: requests.Response, max_time_ms: int):
        actual_time_ms = response.elapsed.total_seconds() * 1000
        assert actual_time_ms <= max_time_ms, \
            f"Response time {actual_time_ms:.2f}ms exceeded maximum allowed {max_time_ms}ms"
    
    @staticmethod
    def assert_header_exists(response: requests.Response, header_name: str):
        assert header_name in response.headers, \
            f"Header '{header_name}' not found in response headers: {list(response.headers.keys())}"
    
    @staticmethod
    def assert_header_value(response: requests.Response, header_name: str, expected_value: str):
        APIAssertions.assert_header_exists(response, header_name)
        actual_value = response.headers[header_name]
        assert actual_value == expected_value, \
            f"Header '{header_name}' expected value '{expected_value}', but got '{actual_value}'"
    
    @staticmethod
    def assert_content_type(response: requests.Response, expected_content_type: str):
        APIAssertions.assert_header_value(response, 'Content-Type', expected_content_type)
    
    @staticmethod
    def assert_json_response(response: requests.Response):
        try:
            response.json()
        except json.JSONDecodeError as e:
            raise AssertionError(f"Response is not valid JSON: {e}. Response text: {response.text[:200]}")
    
    @staticmethod
    def _resolve_json_path(data: Any, json_path: str) -> Any:
        try:
            current = data
            for key in json_path.split('.'):
                if key.isdigit():
                    current = current[int(key)]
                else:
                    current = current[key]
            return current
        except (KeyError, IndexError, TypeError) as e:
            raise AssertionError(f"JSON path '{json_path}' not found in response: {e}")

    @staticmethod
    def assert_json_path_exists(response: requests.Response, json_path: str):
        APIAssertions.assert_json_response(response)
        APIAssertions._resolve_json_path(response.json(), json_path)

    @staticmethod
    def assert_json_path_value(response: requests.Response, json_path: str, expected_value: Any):
        APIAssertions.assert_json_response(response)
        current = APIAssertions._resolve_json_path(response.json(), json_path)
        assert current == expected_value, \
            f"JSON path '{json_path}' expected value '{expected_value}', but got '{current}'"
    
    @staticmethod
    def assert_json_schema(response: requests.Response, schema: Dict[str, Any]):
        APIAssertions.assert_json_response(response)
        data = response.json()
        
        try:
            jsonschema.validate(instance=data, schema=schema)
        except jsonschema.ValidationError as e:
            raise AssertionError(f"JSON schema validation failed: {e.message}")
    
    @staticmethod
    def assert_response_contains(response: requests.Response, text: str):
        assert text in response.text, \
            f"Response does not contain '{text}'. Response: {response.text[:200]}"
    
    @staticmethod
    def assert_response_not_contains(response: requests.Response, text: str):
        assert text not in response.text, \
            f"Response should not contain '{text}'. Response: {response.text[:200]}"
    
    @staticmethod
    def assert_json_array_length(response: requests.Response, json_path: str, expected_length: int):
        APIAssertions.assert_json_response(response)
        current = APIAssertions._resolve_json_path(response.json(), json_path)
        assert isinstance(current, list), \
            f"JSON path '{json_path}' is not an array"
        actual_length = len(current)
        assert actual_length == expected_length, \
            f"Array at '{json_path}' expected length {expected_length}, but got {actual_length}"

    @staticmethod
    def assert_json_value_type(response: requests.Response, json_path: str, expected_type: type):
        APIAssertions.assert_json_response(response)
        current = APIAssertions._resolve_json_path(response.json(), json_path)
        assert isinstance(current, expected_type), \
            f"JSON path '{json_path}' expected type {expected_type.__name__}, but got {type(current).__name__}"
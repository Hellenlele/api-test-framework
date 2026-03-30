# REST API Automation Testing Framework

A comprehensive Python-based framework for REST API testing using pytest, requests, and jsonschema.

## Features

- **HTTP Client Wrapper**: Built on `requests` with support for all HTTP methods
- **Flexible Authentication**: Bearer token, API key, and Basic auth support 
- **Rich Assertions**: Custom assertions for status codes, headers, JSON responses, schemas
- **Environment Management**: YAML-based configuration for multiple environments
- **Test Data Management**: JSON-based test data with schema validation
- **Comprehensive Logging**: Structured logging with file and console output
- **HTML Reports**: Generated with pytest-html

## Quick Start

### 1. Install Dependencies
```bash
cd api_test_framework
pip install -r requirements.txt
```

### 2. Run Tests
```bash
# Run all tests against demo environment (JSONPlaceholder API)
pytest

# Run tests against specific environment
pytest --env=dev

# Run specific test file
pytest tests/test_users_api.py

# Run with verbose output
pytest -v

# Run tests with custom markers
pytest -m smoke
```

### 3. View Reports
After running tests, check the `reports/` directory for:
- `report.html` - HTML test report
- `test_execution.log` - Detailed execution logs

## Framework Structure

```
api_test_framework/
├── framework/
│   ├── api_client.py      # HTTP client wrapper
│   ├── assertions.py      # Custom API assertions
│   ├── base_test.py       # Base test class with fixtures
│   └── config_manager.py  # Configuration management
├── tests/
│   ├── test_users_api.py  # User API tests
│   ├── test_posts_api.py  # Posts API tests
│   └── conftest.py        # pytest configuration
├── config/
│   └── config.yaml        # Environment configurations
├── data/
│   └── test_data.json     # Test data and schemas
├── reports/               # Generated reports
├── requirements.txt       # Dependencies
└── pytest.ini           # pytest settings
```

## Configuration

### Environment Setup
Edit `config/config.yaml` to add your API environments:

```yaml
environments:
  your_api:
    base_url: "https://your-api.com/api/v1"
    timeout: 30
    auth:
      type: "bearer"
      token: "your-token-here"
```

### Test Data
Add test data in `data/test_data.json`:

```json
{
  "your_resource": {
    "valid_data": {
      "name": "Test Resource",
      "value": "test"
    }
  }
}
```

## Writing Tests

### Basic Test Structure
```python
from framework.base_test import BaseAPITest

class TestYourAPI(BaseAPITest):
    
    def test_get_resource(self, api_client, assert_api):
        response = api_client.get("/resource")
        
        assert_api.assert_status_code(response, 200)
        assert_api.assert_json_response(response)
        assert_api.assert_json_path_exists(response, "id")
```

### Available Assertions
```python
# Status code assertions
assert_api.assert_status_code(response, 200)
assert_api.assert_status_code_in(response, [200, 201])

# Response time
assert_api.assert_response_time(response, 2000)  # max 2 seconds

# Headers
assert_api.assert_header_exists(response, "Content-Type")
assert_api.assert_content_type(response, "application/json")

# JSON assertions
assert_api.assert_json_response(response)
assert_api.assert_json_path_exists(response, "data.user.id")
assert_api.assert_json_path_value(response, "status", "success")
assert_api.assert_json_value_type(response, "id", int)

# Schema validation
assert_api.assert_json_schema(response, your_schema)
```

### Using Test Data
```python
def test_create_user(self, api_client, test_data):
    user_data = test_data["users"]["valid_user"]
    response = api_client.post("/users", json_data=user_data)
```

## HTTP Methods

### GET Requests
```python
# Simple GET
response = api_client.get("/users")

# GET with query parameters
response = api_client.get("/users", params={"page": 1, "limit": 10})

# GET with custom headers
response = api_client.get("/users", headers={"X-Custom": "value"})
```

### POST Requests
```python
# POST with JSON data
response = api_client.post("/users", json_data={"name": "John"})

# POST with form data
response = api_client.post("/users", data={"name": "John"})
```

### PUT/PATCH Requests
```python
# Full update
response = api_client.put("/users/1", json_data=complete_user_data)

# Partial update
response = api_client.patch("/users/1", json_data={"name": "Updated"})
```

### DELETE Requests
```python
response = api_client.delete("/users/1")
```

## Authentication

### Bearer Token
```yaml
auth:
  type: "bearer"
  token: "your-jwt-token"
```

### API Key
```yaml
auth:
  type: "api_key"
  key_name: "X-API-Key"
  api_key: "your-api-key"
```

### Basic Auth
```yaml
auth:
  type: "basic"
  username: "user"
  password: "pass"
```

## Environment Variables

Set environment for test execution:
```bash
export TEST_ENV=staging
pytest
```

## Test Markers

Mark tests for selective execution:
```python
@pytest.mark.smoke
def test_health_check(self, api_client):
    pass

@pytest.mark.slow
def test_large_dataset(self, api_client):
    pass
```

Run marked tests:
```bash
pytest -m smoke    # Run only smoke tests
pytest -m "not slow"  # Skip slow tests
```

## Logging

Logs are written to:
- Console (INFO level)
- `reports/test_execution.log` (DEBUG level)

Log format includes timestamp, logger name, level, and message.

## Example Test Output

```
====== test session starts ======
tests/test_users_api.py::TestUsersAPI::test_get_all_users PASSED
tests/test_users_api.py::TestUsersAPI::test_create_user PASSED
tests/test_posts_api.py::TestPostsAPI::test_get_all_posts PASSED

====== 3 passed in 2.45s ======
```

## Best Practices

1. **Use meaningful test names** that describe what's being tested
2. **Group related tests** in classes
3. **Use test data files** instead of hardcoding values
4. **Validate response schemas** for data integrity
5. **Assert response times** for performance requirements
6. **Use appropriate HTTP status codes** in assertions
7. **Log test execution** for debugging and reporting
8. **Organize tests** by API resources or functionality

## Extending the Framework

### Custom Assertions
Add new assertions to `framework/assertions.py`:

```python
@staticmethod
def assert_custom_validation(response, expected_value):
    # Your custom assertion logic
    pass
```

### Custom Fixtures
Add fixtures to `tests/conftest.py`:

```python
@pytest.fixture
def custom_data():
    return {"key": "value"}
```

### Environment-Specific Tests
```python
@pytest.mark.skipif(os.getenv('TEST_ENV') == 'prod', 
                   reason="Skip in production")
def test_destructive_operation(self, api_client):
    pass
```
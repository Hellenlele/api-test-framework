import pytest
from framework.base_test import BaseAPITest


class TestUsersAPI(BaseAPITest):
    
    def test_get_all_users(self, api_client, assert_api, test_data):
        self.log_test_info("Get All Users", "/users", "GET")

        response = api_client.get("/users")
        
        assert_api.assert_status_code(response, 200)
        assert_api.assert_content_type(response, "application/json; charset=utf-8")
        assert_api.assert_json_response(response)
        self.assert_response_time(response, 3000)
        
        users = response.json()
        assert len(users) > 0, "Users list should not be empty"
        
        first_user = users[0]
        assert "id" in first_user
        assert "name" in first_user
        assert "username" in first_user
        assert "email" in first_user
        
        self.log_test_result("Get All Users", True)
    
    def test_get_user_by_id(self, api_client, assert_api):
        self.log_test_info("Get User By ID", "/users/1", "GET")
        
        user_id = 1
        response = api_client.get(f"/users/{user_id}")
        
        assert_api.assert_status_code(response, 200)
        assert_api.assert_json_response(response)
        
        user = response.json()
        assert_api.assert_json_path_value(response, "id", user_id)
        assert_api.assert_json_path_exists(response, "name")
        assert_api.assert_json_path_exists(response, "username")
        assert_api.assert_json_path_exists(response, "email")
        
        self.log_test_result("Get User By ID", True)
    
    def test_get_nonexistent_user(self, api_client, assert_api):
        self.log_test_info("Get Nonexistent User", "/users/999", "GET")
        
        response = api_client.get("/users/999")
        
        assert_api.assert_status_code(response, 404)
        
        self.log_test_result("Get Nonexistent User", True)
    
    def test_create_user(self, api_client, assert_api, test_data):
        self.log_test_info("Create User", "/users", "POST")
        
        user_data = test_data["users"]["valid_user"]
        response = api_client.post("/users", json_data=user_data)
        
        assert_api.assert_status_code(response, 201)
        assert_api.assert_json_response(response)
        
        created_user = response.json()
        assert "id" in created_user, "Created user should have an ID"
        assert_api.assert_json_path_value(response, "name", user_data["name"])
        assert_api.assert_json_path_value(response, "username", user_data["username"])
        assert_api.assert_json_path_value(response, "email", user_data["email"])
        
        self.log_test_result("Create User", True)
    
    def test_update_user(self, api_client, assert_api, test_data):
        self.log_test_info("Update User", "/users/1", "PUT")
        
        user_id = 1
        update_data = test_data["users"]["update_user"]
        response = api_client.put(f"/users/{user_id}", json_data=update_data)
        
        assert_api.assert_status_code(response, 200)
        assert_api.assert_json_response(response)
        
        updated_user = response.json()
        assert_api.assert_json_path_value(response, "id", user_id)
        assert_api.assert_json_path_value(response, "name", update_data["name"])
        assert_api.assert_json_path_value(response, "username", update_data["username"])
        assert_api.assert_json_path_value(response, "email", update_data["email"])
        
        self.log_test_result("Update User", True)
    
    def test_partial_update_user(self, api_client, assert_api):
        self.log_test_info("Partial Update User", "/users/1", "PATCH")
        
        user_id = 1
        patch_data = {"name": "Updated Name"}
        response = api_client.patch(f"/users/{user_id}", json_data=patch_data)
        
        assert_api.assert_status_code(response, 200)
        assert_api.assert_json_response(response)
        
        updated_user = response.json()
        assert_api.assert_json_path_value(response, "id", user_id)
        assert_api.assert_json_path_value(response, "name", patch_data["name"])
        
        self.log_test_result("Partial Update User", True)
    
    def test_delete_user(self, api_client, assert_api):
        self.log_test_info("Delete User", "/users/1", "DELETE")
        
        user_id = 1
        response = api_client.delete(f"/users/{user_id}")
        
        assert_api.assert_status_code(response, 200)
        
        self.log_test_result("Delete User", True)
    
    def test_response_time(self, api_client):
        """Verify that all Users API endpoints respond within 2000ms"""
        endpoints = [
            ("/users", "GET All Users"),
            ("/users/1", "GET User By ID"),
        ]

        for path, name in endpoints:
            response = api_client.get(path)
            self.assert_response_time(response, 2000)

    def test_create_user_with_invalid_data(self, api_client, assert_api, test_data):
        self.log_test_info("Create User Invalid Data", "/users", "POST")
        
        invalid_data = test_data["users"]["invalid_user"]
        response = api_client.post("/users", json_data=invalid_data)
        
        assert_api.assert_status_code_in(response, [400, 422])
        
        self.log_test_result("Create User Invalid Data", True)
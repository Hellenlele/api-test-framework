import pytest
from framework.base_test import BaseAPITest
from schemas.post_schema import CREATE_POST_RESPONSE_SCHEMA


class TestPostsAPI(BaseAPITest):
    
    def test_get_all_posts(self, api_client, assert_api):
        self.log_test_info("Get All Posts", "/posts", "GET")
        
        response = api_client.get("/posts")
        
        assert_api.assert_status_code(response, 200)
        assert_api.assert_content_type(response, "application/json; charset=utf-8")
        assert_api.assert_json_response(response)
        self.assert_response_time(response, 3000)
        
        posts = response.json()
        assert len(posts) > 0, "Posts list should not be empty"
        
        first_post = posts[0]
        assert "id" in first_post
        assert "title" in first_post
        assert "body" in first_post
        assert "userId" in first_post
        
        self.log_test_result("Get All Posts", True)
    
    def test_get_post_by_id(self, api_client, assert_api):
        self.log_test_info("Get Post By ID", "/posts/1", "GET")
        
        post_id = 1
        response = api_client.get(f"/posts/{post_id}")
        
        assert_api.assert_status_code(response, 200)
        assert_api.assert_json_response(response)
        
        assert_api.assert_json_path_value(response, "id", post_id)
        assert_api.assert_json_path_exists(response, "title")
        assert_api.assert_json_path_exists(response, "body")
        assert_api.assert_json_path_exists(response, "userId")
        
        assert_api.assert_json_value_type(response, "id", int)
        assert_api.assert_json_value_type(response, "title", str)
        assert_api.assert_json_value_type(response, "body", str)
        assert_api.assert_json_value_type(response, "userId", int)
        
        self.log_test_result("Get Post By ID", True)
    
    def test_get_posts_by_user(self, api_client, assert_api):
        self.log_test_info("Get Posts By User", "/posts?userId=1", "GET")
        
        user_id = 1
        response = api_client.get("/posts", params={"userId": user_id})
        
        assert_api.assert_status_code(response, 200)
        assert_api.assert_json_response(response)
        
        posts = response.json()
        assert len(posts) > 0, f"User {user_id} should have posts"
        
        for post in posts:
            assert post["userId"] == user_id, f"All posts should belong to user {user_id}"
        
        self.log_test_result("Get Posts By User", True)
    
    def test_create_post(self, api_client, assert_api, test_data):
        self.log_test_info("Create Post", "/posts", "POST")
        
        post_data = test_data["posts"]["valid_post"]
        response = api_client.post("/posts", json_data=post_data)
        
        assert_api.assert_status_code(response, 201)
        assert_api.assert_json_response(response)
        
        created_post = response.json()
        assert "id" in created_post, "Created post should have an ID"
        assert_api.assert_json_path_value(response, "title", post_data["title"])
        assert_api.assert_json_path_value(response, "body", post_data["body"])
        assert_api.assert_json_path_value(response, "userId", post_data["userId"])
        
        self.log_test_result("Create Post", True)
    
    def test_update_post(self, api_client, assert_api, test_data):
        self.log_test_info("Update Post", "/posts/1", "PUT")
        
        post_id = 1
        update_data = test_data["posts"]["update_post"]
        response = api_client.put(f"/posts/{post_id}", json_data=update_data)
        
        assert_api.assert_status_code(response, 200)
        assert_api.assert_json_response(response)
        
        updated_post = response.json()
        assert_api.assert_json_path_value(response, "id", post_id)
        assert_api.assert_json_path_value(response, "title", update_data["title"])
        assert_api.assert_json_path_value(response, "body", update_data["body"])
        assert_api.assert_json_path_value(response, "userId", update_data["userId"])
        
        self.log_test_result("Update Post", True)
    
    def test_partial_update_post(self, api_client, assert_api):
        self.log_test_info("Partial Update Post", "/posts/1", "PATCH")
        
        post_id = 1
        patch_data = {"title": "Updated Post Title"}
        response = api_client.patch(f"/posts/{post_id}", json_data=patch_data)
        
        assert_api.assert_status_code(response, 200)
        assert_api.assert_json_response(response)
        
        updated_post = response.json()
        assert_api.assert_json_path_value(response, "id", post_id)
        assert_api.assert_json_path_value(response, "title", patch_data["title"])
        
        self.log_test_result("Partial Update Post", True)
    
    def test_delete_post(self, api_client, assert_api):
        self.log_test_info("Delete Post", "/posts/1", "DELETE")
        
        post_id = 1
        response = api_client.delete(f"/posts/{post_id}")
        
        assert_api.assert_status_code(response, 200)
        
        self.log_test_result("Delete Post", True)
    
    def test_get_post_comments(self, api_client, assert_api):
        self.log_test_info("Get Post Comments", "/posts/1/comments", "GET")
        
        post_id = 1
        response = api_client.get(f"/posts/{post_id}/comments")
        
        assert_api.assert_status_code(response, 200)
        assert_api.assert_json_response(response)
        
        comments = response.json()
        assert len(comments) >= 0, "Comments should be a list"
        
        if len(comments) > 0:
            first_comment = comments[0]
            assert "id" in first_comment
            assert "name" in first_comment
            assert "email" in first_comment
            assert "body" in first_comment
            assert "postId" in first_comment
            assert first_comment["postId"] == post_id

        self.log_test_result("Get Post Comments", True)

    # ==================== Negative Tests ====================

    def test_get_nonexistent_post(self, api_client, assert_api):
        """Test GET request for a post that doesn't exist"""
        self.log_test_info("Get Nonexistent Post", "/posts/99999", "GET")

        response = api_client.get("/posts/99999")

        assert_api.assert_status_code(response, 404)

        self.log_test_result("Get Nonexistent Post", True)

    def test_create_post_with_invalid_data(self, api_client, assert_api, test_data):
        """Test POST request with invalid data (empty fields, wrong types)"""
        self.log_test_info("Create Post Invalid Data", "/posts", "POST")

        invalid_data = test_data["posts"]["invalid_post"]
        response = api_client.post("/posts", json_data=invalid_data)

        # API should reject invalid data with 400 Bad Request or 422 Unprocessable Entity
        assert_api.assert_status_code_in(response, [400, 422])

        self.log_test_result("Create Post Invalid Data", True)

    def test_create_post_with_missing_required_fields(self, api_client, assert_api, test_data):
        """Test POST request with missing required fields"""
        self.log_test_info("Create Post Missing Fields", "/posts", "POST")

        incomplete_data = test_data["posts"]["post_missing_fields"]
        response = api_client.post("/posts", json_data=incomplete_data)

        # API should reject incomplete data with 400 Bad Request or 422 Unprocessable Entity
        assert_api.assert_status_code_in(response, [400, 422])

        self.log_test_result("Create Post Missing Fields", True)

    def test_create_post_with_empty_body(self, api_client, assert_api):
        """Test POST request with empty request body"""
        self.log_test_info("Create Post Empty Body", "/posts", "POST")

        response = api_client.post("/posts", json_data={})

        # API should reject empty body with 400 Bad Request or 422 Unprocessable Entity
        assert_api.assert_status_code_in(response, [400, 422])

        self.log_test_result("Create Post Empty Body", True)

    def test_update_nonexistent_post(self, api_client, assert_api, test_data):
        """Test PUT request for a post that doesn't exist"""
        self.log_test_info("Update Nonexistent Post", "/posts/99999", "PUT")

        update_data = test_data["posts"]["update_post"]
        response = api_client.put("/posts/99999", json_data=update_data)

        # API should return 404 Not Found for nonexistent resource
        assert_api.assert_status_code(response, 404)

        self.log_test_result("Update Nonexistent Post", True)

    def test_patch_nonexistent_post(self, api_client, assert_api):
        """Test PATCH request for a post that doesn't exist"""
        self.log_test_info("Patch Nonexistent Post", "/posts/99999", "PATCH")

        patch_data = {"title": "Updated Title"}
        response = api_client.patch("/posts/99999", json_data=patch_data)

        # API should return 404 Not Found for nonexistent resource
        assert_api.assert_status_code(response, 404)

        self.log_test_result("Patch Nonexistent Post", True)

    def test_delete_nonexistent_post(self, api_client, assert_api):
        """Test DELETE request for a post that doesn't exist"""
        self.log_test_info("Delete Nonexistent Post", "/posts/99999", "DELETE")

        response = api_client.delete("/posts/99999")

        # API should return 404 Not Found for nonexistent resource
        assert_api.assert_status_code(response, 404)

        self.log_test_result("Delete Nonexistent Post", True)

    def test_get_post_with_invalid_id_format(self, api_client, assert_api):
        """Test GET request with invalid ID format (string instead of integer)"""
        self.log_test_info("Get Post Invalid ID", "/posts/invalid-id", "GET")

        response = api_client.get("/posts/invalid-id")

        # API should return 400 Bad Request or 404 Not Found for invalid ID format
        assert_api.assert_status_code_in(response, [400, 404])

        self.log_test_result("Get Post Invalid ID", True)

    def test_get_posts_by_nonexistent_user(self, api_client, assert_api):
        """Test GET request filtering by a user that doesn't exist"""
        self.log_test_info("Get Posts By Nonexistent User", "/posts?userId=99999", "GET")

        response = api_client.get("/posts", params={"userId": 99999})

        assert_api.assert_status_code(response, 200)
        assert_api.assert_json_response(response)

        # Should return empty array for nonexistent user
        posts = response.json()
        assert len(posts) == 0, "Posts list should be empty for nonexistent user"

        self.log_test_result("Get Posts By Nonexistent User", True)

    def test_response_time(self, api_client):
        """验证 Posts API 各接口响应时间均在 2000ms 以内"""
        endpoints = [
            ("/posts", "GET All Posts"),
            ("/posts/1", "GET Post By ID"),
            ("/posts/1/comments", "GET Post Comments"),
        ]

        for path, name in endpoints:
            response = api_client.get(path)
            self.assert_response_time(response, 2000)

    def test_delete_all_posts_by_user(self, api_client, assert_api):
        """Delete all posts belonging to a particular user"""
        user_id = 1
        self.log_test_info("Delete All Posts By User", f"/posts?userId={user_id}", "DELETE")

        # Fetch all posts for the user
        response = api_client.get("/posts", params={"userId": user_id})
        assert_api.assert_status_code(response, 200)

        posts = response.json()
        assert len(posts) > 0, f"User {user_id} should have posts to delete"

        # Delete each post
        deleted_ids = []
        for post in posts:
            post_id = post["id"]
            delete_response = api_client.delete(f"/posts/{post_id}")
            assert_api.assert_status_code(delete_response, 200)
            deleted_ids.append(post_id)

        assert len(deleted_ids) == len(posts), "All posts should have been deleted"
        self.log_test_result("Delete All Posts By User", True)

    def test_create_post_schema_validation(self, api_client, assert_api):
        """POST /posts 创建文章后，验证响应结构符合预期 schema"""
        self.log_test_info("Create Post Schema Validation", "/posts", "POST")

        payload = {
            "title": "test title",
            "body": "test body content",
            "userId": 1
        }

        response = api_client.post("/posts", json_data=payload)

        assert_api.assert_status_code(response, 201)
        assert_api.assert_json_schema(response, CREATE_POST_RESPONSE_SCHEMA)

        self.log_test_result("Create Post Schema Validation", True)
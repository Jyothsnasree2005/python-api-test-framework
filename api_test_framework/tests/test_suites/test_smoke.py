"""
Smoke Tests — Quick sanity checks against JSONPlaceholder API.
Run: pytest tests/test_suites/test_smoke.py -m smoke -v
"""

import pytest
from core.validator import validate
from utils.data_helpers import make_post_payload, make_user_payload


@pytest.mark.smoke
class TestGetEndpoints:
    def test_get_all_posts(self, api_client):
        response = api_client.get("/posts")
        (validate(response)
            .status_ok()
            .content_type_json()
            .body_is_list()
            .body_list_not_empty()
            .response_time_under(3000))

    def test_get_single_post(self, api_client):
        response = api_client.get("/posts/1")
        (validate(response)
            .status_ok()
            .body_contains_key("id")
            .body_contains_key("title")
            .body_contains_key("body")
            .body_value_equals("id", 1))

    def test_get_users(self, api_client):
        response = api_client.get("/users")
        (validate(response)
            .status_ok()
            .body_is_list()
            .body_list_not_empty())

    def test_get_single_user(self, api_client):
        response = api_client.get("/users/1")
        (validate(response)
            .status_ok()
            .body_contains_key("id")
            .body_contains_key("name")
            .body_contains_key("email")
            .body_value_not_null("name"))

    def test_get_comments_by_post(self, api_client):
        response = api_client.get("/comments", params={"postId": 1})
        (validate(response)
            .status_ok()
            .body_is_list()
            .body_list_not_empty())


@pytest.mark.smoke
class TestPostEndpoints:
    def test_create_post(self, api_client):
        payload = make_post_payload()
        response = api_client.post("/posts", json=payload)
        (validate(response)
            .status_created()
            .body_contains_key("id")
            .body_value_equals("title", payload["title"]))

    def test_create_post_schema(self, api_client):
        schema = {
            "type": "object",
            "required": ["id", "title", "body", "userId"],
            "properties": {
                "id":     {"type": "integer"},
                "title":  {"type": "string"},
                "body":   {"type": "string"},
                "userId": {"type": "integer"},
            }
        }
        payload = make_post_payload()
        response = api_client.post("/posts", json=payload)
        validate(response).status_created().body_matches_schema(schema)


@pytest.mark.smoke
class TestUpdateEndpoints:
    def test_update_post(self, api_client):
        payload = {"id": 1, "title": "Updated Title", "body": "Updated body", "userId": 1}
        response = api_client.put("/posts/1", json=payload)
        (validate(response)
            .status_ok()
            .body_value_equals("title", "Updated Title"))

    def test_patch_post(self, api_client):
        response = api_client.patch("/posts/1", json={"title": "Patched Title"})
        (validate(response)
            .status_ok()
            .body_contains_key("title"))

    def test_delete_post(self, api_client):
        response = api_client.delete("/posts/1")
        validate(response).status_ok()


@pytest.mark.smoke
class TestNegativeCases:
    def test_post_not_found(self, api_client):
        response = api_client.get("/posts/99999")
        validate(response).status_code(404)

    def test_invalid_endpoint(self, api_client):
        response = api_client.get("/nonexistent_endpoint")
        validate(response).status_code(404)

"""
Regression Tests — Comprehensive validation of API behaviour.
Run: pytest tests/test_suites/test_regression.py -m regression -v
"""

import pytest
from core.validator import validate
from utils.data_helpers import make_post_payload, random_email, random_string


@pytest.mark.regression
class TestPostsCRUD:
    """Full CRUD lifecycle for /posts."""

    @pytest.fixture(autouse=True)
    def created_post_id(self, api_client):
        """Create a post and store its ID for use within tests."""
        payload = make_post_payload()
        response = api_client.post("/posts", json=payload)
        validate(response).status_created()
        self.post_id = response.json().get("id")
        self.payload = payload

    def test_read_after_create(self, api_client):
        # JSONPlaceholder doesn't persist, but we validate the pattern
        response = api_client.get(f"/posts/{self.post_id or 1}")
        validate(response).status_ok().body_contains_key("id")

    def test_update_full(self, api_client):
        new_data = make_post_payload(title="Regression Updated", user_id=2)
        response = api_client.put(f"/posts/{self.post_id or 1}", json=new_data)
        validate(response).status_ok()

    def test_partial_update(self, api_client):
        response = api_client.patch(f"/posts/{self.post_id or 1}",
                                    json={"title": "Partially Updated"})
        validate(response).status_ok().body_contains_key("title")

    def test_delete(self, api_client):
        response = api_client.delete(f"/posts/{self.post_id or 1}")
        validate(response).status_ok()


@pytest.mark.regression
class TestQueryFilters:
    """Test query parameter filtering."""

    def test_filter_posts_by_user(self, api_client):
        response = api_client.get("/posts", params={"userId": 1})
        validate(response).status_ok().body_is_list().body_list_not_empty()
        for post in response.json():
            assert post["userId"] == 1, f"Unexpected userId: {post['userId']}"

    def test_filter_comments_by_post(self, api_client):
        response = api_client.get("/comments", params={"postId": 2})
        validate(response).status_ok().body_is_list()
        for comment in response.json():
            assert comment["postId"] == 2

    def test_filter_todos_by_user(self, api_client):
        response = api_client.get("/todos", params={"userId": 1})
        validate(response).status_ok().body_is_list()


@pytest.mark.regression
class TestResponseStructure:
    """Validate response field types and structure."""

    def test_post_fields_have_correct_types(self, api_client):
        response = api_client.get("/posts/1")
        data = response.json()
        validate(response).status_ok()
        assert isinstance(data["id"], int)
        assert isinstance(data["userId"], int)
        assert isinstance(data["title"], str)
        assert isinstance(data["body"], str)

    def test_user_fields_have_correct_types(self, api_client):
        response = api_client.get("/users/1")
        data = response.json()
        validate(response).status_ok()
        assert isinstance(data["id"], int)
        assert isinstance(data["name"], str)
        assert isinstance(data["email"], str)
        assert isinstance(data["address"], dict)


@pytest.mark.regression
class TestPagination:
    """Test that list endpoints return expected counts."""

    def test_all_posts_count(self, api_client):
        response = api_client.get("/posts")
        posts = response.json()
        validate(response).status_ok().body_is_list()
        assert len(posts) == 100, f"Expected 100 posts, got {len(posts)}"

    def test_all_users_count(self, api_client):
        response = api_client.get("/users")
        users = response.json()
        validate(response).status_ok().body_is_list()
        assert len(users) == 10, f"Expected 10 users, got {len(users)}"

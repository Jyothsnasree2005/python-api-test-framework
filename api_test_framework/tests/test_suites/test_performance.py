"""
Performance Tests — Response time assertions.
Run: pytest tests/test_suites/test_performance.py -m performance -v
"""

import time
import pytest
from core.validator import validate
from utils.data_helpers import make_post_payload


@pytest.mark.performance
class TestResponseTimes:
    """Assert endpoints respond within acceptable thresholds."""

    def test_get_posts_under_2s(self, api_client):
        response = api_client.get("/posts")
        validate(response).status_ok().response_time_under(2000)

    def test_get_single_post_under_1s(self, api_client):
        response = api_client.get("/posts/1")
        validate(response).status_ok().response_time_under(1000)

    def test_create_post_under_2s(self, api_client):
        payload = make_post_payload()
        response = api_client.post("/posts", json=payload)
        validate(response).status_created().response_time_under(2000)

    def test_get_users_under_1s(self, api_client):
        response = api_client.get("/users")
        validate(response).status_ok().response_time_under(1000)


@pytest.mark.performance
class TestConcurrentRequests:
    """Run repeated calls and check average response time."""

    def test_average_get_time(self, api_client, iterations: int = 5):
        times = []
        for i in range(iterations):
            response = api_client.get(f"/posts/{i + 1}")
            validate(response).status_ok()
            times.append(response.elapsed.total_seconds() * 1000)

        avg = sum(times) / len(times)
        print(f"\n  Average response time over {iterations} calls: {avg:.0f}ms")
        assert avg < 2000, f"Average response time {avg:.0f}ms exceeds 2000ms threshold"

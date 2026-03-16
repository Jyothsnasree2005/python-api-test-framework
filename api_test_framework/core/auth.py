"""
Auth Manager Module
Handles Bearer tokens, API keys, Basic auth, and OAuth2 client credentials.
"""

import base64
import logging
import time
import requests

logger = logging.getLogger(__name__)


class AuthManager:
    """Manages auth headers and token refresh logic."""

    @staticmethod
    def bearer_header(token: str) -> dict:
        return {"Authorization": f"Bearer {token}"}

    @staticmethod
    def api_key_header(api_key: str, header_name: str = "X-API-Key") -> dict:
        return {header_name: api_key}

    @staticmethod
    def basic_header(username: str, password: str) -> dict:
        encoded = base64.b64encode(f"{username}:{password}".encode()).decode()
        return {"Authorization": f"Basic {encoded}"}

    @staticmethod
    def fetch_oauth2_token(token_url: str, client_id: str, client_secret: str,
                           scope: str = "") -> str:
        """Fetch an OAuth2 access token using client_credentials grant."""
        payload = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
        }
        if scope:
            payload["scope"] = scope

        response = requests.post(token_url, data=payload, timeout=30)
        response.raise_for_status()
        token = response.json().get("access_token")
        if not token:
            raise ValueError("No access_token found in OAuth2 response")
        logger.info("OAuth2 token fetched successfully")
        return token


class TokenCache:
    """Simple in-memory token cache with TTL."""

    def __init__(self):
        self._cache: dict = {}

    def get(self, key: str) -> str | None:
        entry = self._cache.get(key)
        if entry and time.time() < entry["expires_at"]:
            return entry["token"]
        return None

    def set(self, key: str, token: str, ttl_seconds: int = 3600):
        self._cache[key] = {"token": token, "expires_at": time.time() + ttl_seconds}

    def invalidate(self, key: str):
        self._cache.pop(key, None)

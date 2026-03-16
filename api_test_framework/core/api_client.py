"""
Core API Client Module
Handles all HTTP interactions with retry, timeout, and auth support.
"""

import requests
import logging
from typing import Any, Optional
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)


class APIClient:
    def __init__(self, base_url: str, auth_type: str = None, token: str = None,
                 api_key: str = None, api_key_header: str = "X-API-Key",
                 timeout: int = 30, retries: int = 3):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()

        # Retry strategy
        retry = Retry(total=retries, backoff_factor=0.3,
                      status_forcelist=[500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        # Auth setup
        if auth_type == "bearer" and token:
            self.session.headers.update({"Authorization": f"Bearer {token}"})
        elif auth_type == "api_key" and api_key:
            self.session.headers.update({api_key_header: api_key})

        self.session.headers.update({"Content-Type": "application/json", "Accept": "application/json"})

    def _request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        logger.info(f"[{method.upper()}] {url} | params={kwargs.get('params')} | body={kwargs.get('json')}")
        response = self.session.request(method, url, timeout=self.timeout, **kwargs)
        logger.info(f"Response [{response.status_code}] — {len(response.content)} bytes")
        return response

    def get(self, endpoint: str, params: dict = None, headers: dict = None) -> requests.Response:
        return self._request("GET", endpoint, params=params, headers=headers)

    def post(self, endpoint: str, json: Any = None, data: Any = None, headers: dict = None) -> requests.Response:
        return self._request("POST", endpoint, json=json, data=data, headers=headers)

    def put(self, endpoint: str, json: Any = None, headers: dict = None) -> requests.Response:
        return self._request("PUT", endpoint, json=json, headers=headers)

    def patch(self, endpoint: str, json: Any = None, headers: dict = None) -> requests.Response:
        return self._request("PATCH", endpoint, json=json, headers=headers)

    def delete(self, endpoint: str, headers: dict = None) -> requests.Response:
        return self._request("DELETE", endpoint, headers=headers)

    def close(self):
        self.session.close()

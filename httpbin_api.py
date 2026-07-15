from __future__ import annotations

from typing import Any

from api_client import ApiClient


class HttpbinApi:
    @staticmethod
    def get_request_info() -> dict[str, Any]:
        # httpbin.org's shared demo instance is frequently overloaded (503s);
        # httpbingo.org is a compatible reimplementation that responds reliably.
        url = "https://httpbingo.org/get"
        return ApiClient.fetch_json(url)


def get_request_info() -> dict[str, Any]:
    return HttpbinApi.get_request_info()

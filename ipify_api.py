from __future__ import annotations

from typing import Any

from api_client import ApiClient


class IpifyApi:
    @staticmethod
    def get_public_ip() -> dict[str, Any]:
        url = "https://api.ipify.org?format=json"
        return ApiClient.fetch_json(url)


def get_public_ip() -> dict[str, Any]:
    return IpifyApi.get_public_ip()

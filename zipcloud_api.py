from __future__ import annotations

from typing import Any

from api_client import ApiClient


class ZipcloudApi:
    @staticmethod
    def get_address(zipcode: str) -> dict[str, Any]:
        url = f"https://zipcloud.ibsnet.co.jp/api/search?zipcode={zipcode.strip()}"
        return ApiClient.fetch_json(url)


def get_address(zipcode: str) -> dict[str, Any]:
    return ZipcloudApi.get_address(zipcode)

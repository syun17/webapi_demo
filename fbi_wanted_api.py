from __future__ import annotations

from typing import Any

from api_client import ApiClient


class FbiWantedApi:
    @staticmethod
    def get_wanted_list(page_size: int = 10) -> dict[str, Any]:
        url = f"https://api.fbi.gov/wanted/v1/list?pageSize={page_size}"
        return ApiClient.fetch_json(url)


def get_wanted_list(page_size: int = 10) -> dict[str, Any]:
    return FbiWantedApi.get_wanted_list(page_size)

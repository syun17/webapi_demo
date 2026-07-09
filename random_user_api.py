from __future__ import annotations

from typing import Any

from api_client import ApiClient


class RandomUserApi:
    @staticmethod
    def get_random_user() -> dict[str, Any]:
        url = "https://randomuser.me/api/"
        return ApiClient.fetch_json(url)


def get_random_user() -> dict[str, Any]:
    return RandomUserApi.get_random_user()
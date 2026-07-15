from __future__ import annotations

from typing import Any

from api_client import ApiClient


class ChuckNorrisApi:
    @staticmethod
    def get_random_joke(category: str | None = None) -> dict[str, Any]:
        url = "https://api.chucknorris.io/jokes/random"
        if category:
            url += f"?category={category.strip()}"
        return ApiClient.fetch_json(url)


def get_random_joke(category: str | None = None) -> dict[str, Any]:
    return ChuckNorrisApi.get_random_joke(category)

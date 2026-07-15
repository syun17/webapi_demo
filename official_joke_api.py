from __future__ import annotations

from typing import Any

from api_client import ApiClient


class OfficialJokeApi:
    @staticmethod
    def get_random_joke() -> dict[str, Any]:
        url = "https://official-joke-api.appspot.com/random_joke"
        return ApiClient.fetch_json(url)


def get_random_joke() -> dict[str, Any]:
    return OfficialJokeApi.get_random_joke()

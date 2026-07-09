from __future__ import annotations

from typing import Any

from api_client import ApiClient


class DadJokeApi:
    @staticmethod
    def get_joke() -> dict[str, Any]:
        url = "https://icanhazdadjoke.com/slack"
        return ApiClient.fetch_json(url, headers={"Accept": "application/json"})


def get_joke() -> dict[str, Any]:
    return DadJokeApi.get_joke()
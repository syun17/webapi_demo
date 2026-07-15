from __future__ import annotations

from typing import Any

from api_client import ApiClient


class DatamuseApi:
    @staticmethod
    def get_related_words(word: str) -> list[dict[str, Any]]:
        url = f"https://api.datamuse.com/words?ml={word.strip()}"
        return ApiClient.fetch_json(url)


def get_related_words(word: str) -> list[dict[str, Any]]:
    return DatamuseApi.get_related_words(word)

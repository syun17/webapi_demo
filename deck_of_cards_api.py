from __future__ import annotations

from typing import Any

from api_client import ApiClient


class DeckOfCardsApi:
    @staticmethod
    def shuffle_new_deck(deck_count: int = 1) -> dict[str, Any]:
        url = f"https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count={deck_count}"
        return ApiClient.fetch_json(url)


def shuffle_new_deck(deck_count: int = 1) -> dict[str, Any]:
    return DeckOfCardsApi.shuffle_new_deck(deck_count)

from __future__ import annotations

from typing import Any

from api_client import ApiClient


class QuoteApi:
	@staticmethod
	def get_quote() -> dict[str, Any]:
		url = "https://dummyjson.com/quotes/random"
		return ApiClient.fetch_json(url)


def get_quote() -> dict[str, Any]:
	return QuoteApi.get_quote()
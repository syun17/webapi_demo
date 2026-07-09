from __future__ import annotations

from typing import Any

from api_client import ApiClient


class PokemonApi:
    @staticmethod
    def get_pokemon(name: str) -> dict[str, Any]:
        url = f"https://pokeapi.co/api/v2/pokemon/{name.strip().lower()}"
        data = ApiClient.fetch_json(url)
        return {
            "name": data["name"],
            "id": data["id"],
            "types": [item["type"]["name"] for item in data["types"]],
            "image": data["sprites"]["front_default"],
            "height": data["height"],
            "weight": data["weight"],
        }

    @staticmethod
    def get_pokemon_name_options(limit: int = 30) -> list[dict[str, str]]:
        data = ApiClient.fetch_json(f"https://pokeapi.co/api/v2/pokemon?limit={limit}&offset=0")
        return [{"value": item["name"], "label": item["name"].title()} for item in data.get("results", [])]


def get_pokemon(name: str) -> dict[str, Any]:
    return PokemonApi.get_pokemon(name)


def get_pokemon_name_options(limit: int = 30) -> list[dict[str, str]]:
    return PokemonApi.get_pokemon_name_options(limit)
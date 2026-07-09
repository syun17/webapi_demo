from __future__ import annotations

from datetime import datetime
from typing import Any

import requests


DEFAULT_WEATHER_AREA_CODE = "270000"


def fetch_json(url: str, *, headers: dict[str, str] | None = None, timeout: int = 10) -> Any:
    response = requests.get(url, headers=headers, timeout=timeout)
    response.raise_for_status()
    return response.json()


def get_weather(area_code: str = DEFAULT_WEATHER_AREA_CODE) -> dict[str, Any]:
    url = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{area_code}.json"
    root = fetch_json(url)
    first_series = root[0]["timeSeries"][0]
    area = first_series["areas"][0]
    weather_items = []

    for time_value, weather in zip(first_series["timeDefines"], area["weathers"]):
        dt = datetime.fromisoformat(time_value)
        weather_items.append(
            {
                "date": dt.strftime("%Y/%m/%d(%a)"),
                "weather": weather,
            }
        )

    return {
        "area_code": area_code,
        "area_name": area.get("area", {}).get("name", "不明"),
        "items": weather_items,
    }


def get_weather_area_options() -> list[dict[str, str]]:
    data = fetch_json("https://www.jma.go.jp/bosai/common/const/area.json")
    offices = data.get("offices", {})
    options = []

    for code, office in offices.items():
        name = office.get("name") or code
        options.append({"value": code, "label": f"{name} ({code})"})

    return sorted(options, key=lambda item: item["label"])


def get_pokemon(name: str) -> dict[str, Any]:
    url = f"https://pokeapi.co/api/v2/pokemon/{name.strip().lower()}"
    data = fetch_json(url)
    return {
        "name": data["name"],
        "id": data["id"],
        "types": [item["type"]["name"] for item in data["types"]],
        "image": data["sprites"]["front_default"],
        "height": data["height"],
        "weight": data["weight"],
    }


def get_pokemon_name_options(limit: int = 30) -> list[dict[str, str]]:
    data = fetch_json(f"https://pokeapi.co/api/v2/pokemon?limit={limit}&offset=0")
    return [{"value": item["name"], "label": item["name"].title()} for item in data.get("results", [])]


def get_post(post_id: int) -> dict[str, Any]:
    url = f"https://jsonplaceholder.typicode.com/posts/{post_id}"
    return fetch_json(url)


def get_post_id_options(limit: int = 10) -> list[dict[str, str]]:
    data = fetch_json("https://jsonplaceholder.typicode.com/posts")
    unique_ids = []
    seen_ids = set()

    for item in data:
        post_id = item.get("id")
        if post_id in seen_ids:
            continue
        seen_ids.add(post_id)
        unique_ids.append({"value": str(post_id), "label": str(post_id)})
        if len(unique_ids) >= limit:
            break

    return unique_ids


def get_joke() -> dict[str, Any]:
    url = "https://icanhazdadjoke.com/slack"
    return fetch_json(url, headers={"Accept": "application/json"})


def get_country(name: str) -> list[dict[str, Any]]:
    url = f"https://restcountries.com/v3.1/name/{name.strip()}"
    return fetch_json(url)


def get_country_name_options(limit: int = 20) -> list[dict[str, str]]:
    data = fetch_json("https://restcountries.com/v3.1/all?fields=name")
    options = []

    for item in data[:limit]:
        country_name = item.get("name", {}).get("common")
        if country_name:
            options.append({"value": country_name, "label": country_name})

    return sorted(options, key=lambda item: item["label"])


def get_random_user() -> dict[str, Any]:
    url = "https://randomuser.me/api/"
    return fetch_json(url)


def get_picsum_url(width: int = 800, height: int = 500, grayscale: bool = False, blur: int | None = None) -> str:
    params = []
    if grayscale:
        params.append("grayscale")
    if blur is not None:
        params.append(f"blur={blur}")
    query = ""
    if params:
        query = "?" + "&".join(params)
    return f"https://picsum.photos/{width}/{height}{query}"
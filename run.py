from __future__ import annotations

import json

from flask import Flask, render_template, request

from wether import (
	get_country,
	get_country_name_options,
	get_joke,
	get_picsum_url,
	get_post_id_options,
	get_post,
	get_pokemon,
	get_pokemon_name_options,
	get_random_user,
	get_quote,
	get_weather_area_options,
	get_weather,
)

app = Flask(__name__)


def format_json_value(value, *, label=None, depth=0, max_depth=4, max_items=8):
	if depth >= max_depth:
		return {
			"type": "primitive",
			"label": label,
			"value": "...",
		}

	if isinstance(value, dict):
		return {
			"type": "object",
			"label": label,
			"size": len(value),
			"children": [
				format_json_value(item_value, label=str(item_key), depth=depth + 1, max_depth=max_depth, max_items=max_items)
				for item_key, item_value in value.items()
			],
		}

	if isinstance(value, list):
		items = [
			format_json_value(item, label=f"[{index}]", depth=depth + 1, max_depth=max_depth, max_items=max_items)
			for index, item in enumerate(value[:max_items])
		]
		return {
			"type": "array",
			"label": label,
			"size": len(value),
			"children": items,
			"truncated": len(value) > max_items,
		}

	if value is None:
		display_value = "null"
	elif isinstance(value, bool):
		display_value = "true" if value else "false"
	else:
		display_value = str(value)

	return {
		"type": "primitive",
		"label": label,
		"value": display_value,
	}


def format_json_data(data):
	return format_json_value(data)


API_CARDS = [
	{
		"title": "気象庁 天気予報API",
		"description": "予報区コードを指定して今日の天気予報を取得します。",
		"path": "/weather",
		"placeholder": "270000",
	},
	{
		"title": "PokeAPI",
		"description": "ポケモン名を指定して、タイプや図鑑情報を取得します。",
		"path": "/pokemon",
		"placeholder": "pikachu",
	},
	{
		"title": "JSONPlaceholder",
		"description": "投稿IDを指定してテスト用投稿データを取得します。",
		"path": "/post",
		"placeholder": "1",
	},
	{
		"title": "Icanhazdadjoke API",
		"description": "ランダムなダジャレを取得します。",
		"path": "/joke",
		"placeholder": "",
	},
	{
		"title": "DummyJSON Quotes API",
		"description": "ランダムな名言や引用文を取得します。",
		"path": "/quote",
		"placeholder": "",
	},
	{
		"title": "REST Countries API",
		"description": "国名を指定して首都や人口などの情報を取得します。",
		"path": "/country",
		"placeholder": "Japan",
	},
	{
		"title": "Random User API",
		"description": "ランダムなユーザー情報を取得します。",
		"path": "/user",
		"placeholder": "",
	},
	{
		"title": "Lorem Picsum",
		"description": "ランダムな画像URLを生成して表示します。",
		"path": "/image",
		"placeholder": "",
	},
]

IMAGE_WIDTHS = [
	{"value": "320", "label": "320"},
	{"value": "640", "label": "640"},
	{"value": "800", "label": "800"},
]

IMAGE_HEIGHTS = [
	{"value": "180", "label": "180"},
	{"value": "360", "label": "360"},
	{"value": "500", "label": "500"},
]

IMAGE_BLURS = [
	{"value": "", "label": "なし"},
	{"value": "1", "label": "1"},
	{"value": "2", "label": "2"},
	{"value": "3", "label": "3"},
]


def render_page(template_name, **context):
	if context.get("result") is not None and "formatted_result" not in context:
		context["formatted_result"] = format_json_data(context["result"])
	return render_template(
		template_name,
		api_cards=API_CARDS,
		api_card_count=len(API_CARDS),
		image_widths=IMAGE_WIDTHS,
		image_heights=IMAGE_HEIGHTS,
		image_blurs=IMAGE_BLURS,
		**context,
	)


@app.get("/")
def index():
	return render_page("home.html", page_key="home", page_title="WebAPI Demo")


@app.get("/weather")
def weather():
	try:
		weather_area_codes = get_weather_area_options()
		area_code = request.args.get("area_code", weather_area_codes[0]["value"] if weather_area_codes else "270000").strip() or "270000"
		data = get_weather(area_code)
		summary = f"{data['area_name']} の天気予報を取得しました。"
		return render_page(
			"weather.html",
			page_key="weather",
			page_title="気象庁 天気予報API",
			weather_area_codes=weather_area_codes,
			selected_area_code=area_code,
			summary=summary,
			result=data,
			result_json=json.dumps(data, ensure_ascii=False, indent=2),
		)
	except Exception as exc:  # noqa: BLE001
		return render_page(
			"weather.html",
			page_key="weather",
			page_title="気象庁 天気予報API",
			weather_area_codes=[],
			error=str(exc),
		)


@app.get("/pokemon")
def pokemon():
	try:
		pokemon_names = get_pokemon_name_options()
		name = request.args.get("name", pokemon_names[0]["value"] if pokemon_names else "pikachu").strip() or "pikachu"
		data = get_pokemon(name)
		summary = f"{data['name'].title()} の情報を取得しました。"
		return render_page(
			"pokemon.html",
			page_key="pokemon",
			page_title="PokeAPI",
			pokemon_names=pokemon_names,
			selected_pokemon_name=name,
			summary=summary,
			result=data,
			result_json=json.dumps(data, ensure_ascii=False, indent=2),
		)
	except Exception as exc:  # noqa: BLE001
		return render_page(
			"pokemon.html",
			page_key="pokemon",
			page_title="PokeAPI",
			pokemon_names=[],
			error=str(exc),
		)


@app.get("/post")
def post():
	try:
		post_ids = get_post_id_options()
		post_id = request.args.get("post_id", post_ids[0]["value"] if post_ids else "1").strip() or "1"
		data = get_post(int(post_id))
		summary = f"投稿ID {data['id']} のデータを取得しました。"
		return render_page(
			"post.html",
			page_key="post",
			page_title="JSONPlaceholder",
			post_ids=post_ids,
			selected_post_id=post_id,
			summary=summary,
			result=data,
			result_json=json.dumps(data, ensure_ascii=False, indent=2),
		)
	except Exception as exc:  # noqa: BLE001
		return render_page(
			"post.html",
			page_key="post",
			page_title="JSONPlaceholder",
			post_ids=[],
			error=str(exc),
		)


@app.get("/joke")
def joke():
	try:
		data = get_joke()
		summary = data["attachments"][0]["text"] if data.get("attachments") else "ダジャレを取得しました。"
		return render_page(
			"joke.html",
			page_key="joke",
			page_title="Icanhazdadjoke API",
			summary=summary,
			result=data,
			result_json=json.dumps(data, ensure_ascii=False, indent=2),
		)
	except Exception as exc:  # noqa: BLE001
		return render_page(
			"joke.html",
			page_key="joke",
			page_title="Icanhazdadjoke API",
			error=str(exc),
		)


@app.get("/quote")
def quote():
	try:
		data = get_quote()
		summary = f"{data.get('author', '不明な作者')} の名言を取得しました。"
		return render_page(
			"quote.html",
			page_key="quote",
			page_title="DummyJSON Quotes API",
			summary=summary,
			result=data,
			result_json=json.dumps(data, ensure_ascii=False, indent=2),
		)
	except Exception as exc:  # noqa: BLE001
		return render_page(
			"quote.html",
			page_key="quote",
			page_title="DummyJSON Quotes API",
			error=str(exc),
		)


@app.get("/country")
def country():
	try:
		country_names = get_country_name_options()
		name = request.args.get("name", country_names[0]["value"] if country_names else "Japan").strip() or "Japan"
		data = get_country(name)
		first = data[0]
		# テンプレート用に国情報を抽出
		country_info = {
			"common": first.get("name", {}).get("common", ""),
			"capital": first.get("capital", []),
			"region": first.get("region", ""),
			"population": first.get("population"),
			"languages": list(first.get("languages", {}).values()) if first.get("languages") else [],
			"flags": first.get("flags", {}),
		}
		summary = f"{first['name']['common']} の情報を取得しました。"
		return render_page(
			"country.html",
			page_key="country",
			page_title="REST Countries API",
			country_names=country_names,
			selected_country_name=name,
			summary=summary,
			result=data,
			country_info=country_info,
			result_json=json.dumps(data, ensure_ascii=False, indent=2),
		)
	except Exception as exc:  # noqa: BLE001
		return render_page(
			"country.html",
			page_key="country",
			page_title="REST Countries API",
			country_names=[],
			error=str(exc),
		)


@app.get("/user")
def user():
	try:
		data = get_random_user()
		# テンプレート用にユーザー情報を抽出
		user_data = data.get("results", [{}])[0]
		user_info = {
			"name": f"{user_data.get('name', {}).get('first', '')} {user_data.get('name', {}).get('last', '')}",
			"email": user_data.get("email", ""),
			"login": user_data.get("login", {}).get("username", ""),
			"phone": user_data.get("phone", ""),
			"country": user_data.get("location", {}).get("country", ""),
			"picture": user_data.get("picture", {}).get("large", ""),
		}
		summary = "ランダムユーザーを取得しました。"
		return render_page(
			"user.html",
			page_key="user",
			page_title="Random User API",
			summary=summary,
			result=data,
			user_info=user_info,
			result_json=json.dumps(data, ensure_ascii=False, indent=2),
		)
	except Exception as exc:  # noqa: BLE001
		return render_page(
			"user.html",
			page_key="user",
			page_title="Random User API",
			error=str(exc),
		)


@app.get("/image")
def image():
	width = request.args.get("width", "800").strip() or "800"
	height = request.args.get("height", "500").strip() or "500"
	grayscale = request.args.get("grayscale") == "on"
	blur = request.args.get("blur", "").strip()
	try:
		width_value = max(100, int(width))
		height_value = max(100, int(height))
		blur_value = int(blur) if blur else None
		image_url = get_picsum_url(width_value, height_value, grayscale=grayscale, blur=blur_value)
		summary = f"{width_value} x {height_value} の画像URLを生成しました。"
		result = {
			"width": width_value,
			"height": height_value,
			"grayscale": grayscale,
			"blur": blur_value,
			"url": image_url,
		}
		return render_page(
			"image.html",
			page_key="image",
			page_title="Lorem Picsum",
			summary=summary,
			result=result,
			result_json=json.dumps(result, ensure_ascii=False, indent=2),
			image_url=image_url,
			image_width=width_value,
			image_height=height_value,
		)
	except Exception as exc:  # noqa: BLE001
		return render_page(
			"image.html",
			page_key="image",
			page_title="Lorem Picsum",
			error=str(exc),
		)


if __name__ == "__main__":
	app.run(host="127.0.0.1", port=5000, debug=True)
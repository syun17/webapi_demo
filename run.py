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
	get_wanted_list,
	get_age_prediction,
	get_official_random_joke,
	get_zipcloud_address,
	search_location,
	get_avatar_url,
	get_activity,
	get_related_words,
	search_universities,
	get_postal_info,
	get_public_ip,
	get_iss_location,
	get_astronauts,
	get_request_info,
	get_products,
	get_all_countries,
	shuffle_new_deck,
	get_chuck_norris_joke,
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
	{
		"title": "FBI Wanted API",
		"description": "FBIが公開している指名手配者情報を取得します。",
		"path": "/fbi-wanted",
		"placeholder": "",
	},
	{
		"title": "Agify API",
		"description": "名前から推定年齢を取得します。",
		"path": "/agify",
		"placeholder": "michael",
	},
	{
		"title": "Official Joke API",
		"description": "ランダムな英語のジョークを取得します。",
		"path": "/official-joke",
		"placeholder": "",
	},
	{
		"title": "zipcloud",
		"description": "郵便番号から住所を取得します。",
		"path": "/zipcloud",
		"placeholder": "1000001",
	},
	{
		"title": "Nominatim (OpenStreetMap)",
		"description": "地名・住所から緯度経度を検索します。",
		"path": "/nominatim",
		"placeholder": "Tokyo Tower",
	},
	{
		"title": "UI Avatars",
		"description": "名前のイニシャルからアバター画像を生成します。",
		"path": "/ui-avatars",
		"placeholder": "Taro Yamada",
	},
	{
		"title": "Bored API",
		"description": "暇つぶしのアクティビティ案を取得します。",
		"path": "/bored",
		"placeholder": "",
	},
	{
		"title": "DataMuse API",
		"description": "意味が似ている英単語を検索します。",
		"path": "/datamuse",
		"placeholder": "happy",
	},
	{
		"title": "University Domains API",
		"description": "国名から大学一覧を検索します。",
		"path": "/university",
		"placeholder": "Japan",
	},
	{
		"title": "Zippopotam.us API",
		"description": "国コードと郵便番号から住所情報を取得します。",
		"path": "/zippopotamus",
		"placeholder": "90210",
	},
	{
		"title": "IPify API",
		"description": "サーバーのグローバルIPアドレスを取得します。",
		"path": "/ipify",
		"placeholder": "",
	},
	{
		"title": "Open Notify API (ISS)",
		"description": "国際宇宙ステーションの現在位置を取得します。",
		"path": "/iss-location",
		"placeholder": "",
	},
	{
		"title": "Open Notify Astronaut API",
		"description": "現在宇宙に滞在中の宇宙飛行士一覧を取得します。",
		"path": "/astronauts",
		"placeholder": "",
	},
	{
		"title": "HTTPBin API",
		"description": "HTTPリクエストの内容を確認します。",
		"path": "/httpbin",
		"placeholder": "",
	},
	{
		"title": "Fake Store API",
		"description": "ダミーの商品情報を取得します。",
		"path": "/fake-store",
		"placeholder": "5",
	},
	{
		"title": "Countries Now API",
		"description": "世界各国と都市の一覧を取得します。",
		"path": "/countries-now",
		"placeholder": "",
	},
	{
		"title": "Deck of Cards API",
		"description": "シャッフル済みのトランプの新しいデッキを取得します。",
		"path": "/deck-of-cards",
		"placeholder": "1",
	},
	{
		"title": "Chuck Norris API",
		"description": "チャック・ノリスに関するジョークを取得します。",
		"path": "/chuck-norris",
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


@app.get("/fbi-wanted")
def fbi_wanted():
	try:
		data = get_wanted_list()
		items = data.get("items", [])
		summary = f"{data.get('total', len(items))}件の指名手配情報のうち{len(items)}件を取得しました。"
		return render_page(
			"fbi_wanted.html",
			page_key="fbi-wanted",
			page_title="FBI Wanted API",
			summary=summary,
			result=data,
			wanted_items=items[:10],
			result_json=json.dumps(data, ensure_ascii=False, indent=2),
		)
	except Exception as exc:  # noqa: BLE001
		return render_page(
			"fbi_wanted.html",
			page_key="fbi-wanted",
			page_title="FBI Wanted API",
			error=str(exc),
		)


@app.get("/agify")
def agify():
	name = request.args.get("name", "michael").strip() or "michael"
	try:
		data = get_age_prediction(name)
		summary = f"{data.get('name')} さんの推定年齢は {data.get('age')} 歳です。"
		return render_page(
			"agify.html",
			page_key="agify",
			page_title="Agify API",
			selected_name=name,
			summary=summary,
			result=data,
			result_json=json.dumps(data, ensure_ascii=False, indent=2),
		)
	except Exception as exc:  # noqa: BLE001
		return render_page(
			"agify.html",
			page_key="agify",
			page_title="Agify API",
			selected_name=name,
			error=str(exc),
		)


@app.get("/official-joke")
def official_joke():
	try:
		data = get_official_random_joke()
		summary = data.get("setup", "ジョークを取得しました。")
		return render_page(
			"official_joke.html",
			page_key="official-joke",
			page_title="Official Joke API",
			summary=summary,
			result=data,
			result_json=json.dumps(data, ensure_ascii=False, indent=2),
		)
	except Exception as exc:  # noqa: BLE001
		return render_page(
			"official_joke.html",
			page_key="official-joke",
			page_title="Official Joke API",
			error=str(exc),
		)


@app.get("/zipcloud")
def zipcloud():
	zipcode = request.args.get("zipcode", "1000001").strip() or "1000001"
	try:
		data = get_zipcloud_address(zipcode)
		results = data.get("results") or []
		summary = f"{results[0]['address1']}{results[0]['address2']}{results[0]['address3']} を取得しました。" if results else "該当する住所が見つかりませんでした。"
		return render_page(
			"zipcloud.html",
			page_key="zipcloud",
			page_title="zipcloud",
			selected_zipcode=zipcode,
			summary=summary,
			result=data,
			result_json=json.dumps(data, ensure_ascii=False, indent=2),
		)
	except Exception as exc:  # noqa: BLE001
		return render_page(
			"zipcloud.html",
			page_key="zipcloud",
			page_title="zipcloud",
			selected_zipcode=zipcode,
			error=str(exc),
		)


@app.get("/nominatim")
def nominatim():
	query = request.args.get("query", "Tokyo Tower").strip() or "Tokyo Tower"
	try:
		data = search_location(query)
		summary = f"{len(data)}件の候補地が見つかりました。" if data else "候補地が見つかりませんでした。"
		return render_page(
			"nominatim.html",
			page_key="nominatim",
			page_title="Nominatim (OpenStreetMap)",
			selected_query=query,
			summary=summary,
			result=data,
			result_json=json.dumps(data, ensure_ascii=False, indent=2),
		)
	except Exception as exc:  # noqa: BLE001
		return render_page(
			"nominatim.html",
			page_key="nominatim",
			page_title="Nominatim (OpenStreetMap)",
			selected_query=query,
			error=str(exc),
		)


@app.get("/ui-avatars")
def ui_avatars():
	name = request.args.get("name", "Taro Yamada").strip() or "Taro Yamada"
	try:
		avatar_url = get_avatar_url(name)
		summary = f"{name} のアバター画像URLを生成しました。"
		result = {"name": name, "url": avatar_url}
		return render_page(
			"ui_avatars.html",
			page_key="ui-avatars",
			page_title="UI Avatars",
			selected_name=name,
			summary=summary,
			result=result,
			result_json=json.dumps(result, ensure_ascii=False, indent=2),
			avatar_url=avatar_url,
		)
	except Exception as exc:  # noqa: BLE001
		return render_page(
			"ui_avatars.html",
			page_key="ui-avatars",
			page_title="UI Avatars",
			selected_name=name,
			error=str(exc),
		)


@app.get("/bored")
def bored():
	try:
		data = get_activity()
		summary = data.get("activity", "アクティビティを取得しました。")
		return render_page(
			"bored.html",
			page_key="bored",
			page_title="Bored API",
			summary=summary,
			result=data,
			result_json=json.dumps(data, ensure_ascii=False, indent=2),
		)
	except Exception as exc:  # noqa: BLE001
		return render_page(
			"bored.html",
			page_key="bored",
			page_title="Bored API",
			error=str(exc),
		)


@app.get("/datamuse")
def datamuse():
	word = request.args.get("word", "happy").strip() or "happy"
	try:
		data = get_related_words(word)
		summary = f"「{word}」に関連する単語を{len(data)}件取得しました。"
		return render_page(
			"datamuse.html",
			page_key="datamuse",
			page_title="DataMuse API",
			selected_word=word,
			summary=summary,
			result=data,
			result_json=json.dumps(data, ensure_ascii=False, indent=2),
		)
	except Exception as exc:  # noqa: BLE001
		return render_page(
			"datamuse.html",
			page_key="datamuse",
			page_title="DataMuse API",
			selected_word=word,
			error=str(exc),
		)


@app.get("/university")
def university():
	country = request.args.get("country", "Japan").strip() or "Japan"
	try:
		data = search_universities(country)
		summary = f"{country} の大学を{len(data)}件取得しました。"
		return render_page(
			"university.html",
			page_key="university",
			page_title="University Domains API",
			selected_country=country,
			summary=summary,
			result=data[:20],
			result_json=json.dumps(data[:20], ensure_ascii=False, indent=2),
		)
	except Exception as exc:  # noqa: BLE001
		return render_page(
			"university.html",
			page_key="university",
			page_title="University Domains API",
			selected_country=country,
			error=str(exc),
		)


@app.get("/zippopotamus")
def zippopotamus():
	country = request.args.get("country", "us").strip() or "us"
	postal_code = request.args.get("postal_code", "90210").strip() or "90210"
	try:
		data = get_postal_info(country, postal_code)
		summary = f"{data.get('place name', '')} の住所情報を取得しました。"
		return render_page(
			"zippopotamus.html",
			page_key="zippopotamus",
			page_title="Zippopotam.us API",
			selected_country=country,
			selected_postal_code=postal_code,
			summary=summary,
			result=data,
			result_json=json.dumps(data, ensure_ascii=False, indent=2),
		)
	except Exception as exc:  # noqa: BLE001
		return render_page(
			"zippopotamus.html",
			page_key="zippopotamus",
			page_title="Zippopotam.us API",
			selected_country=country,
			selected_postal_code=postal_code,
			error=str(exc),
		)


@app.get("/ipify")
def ipify():
	try:
		data = get_public_ip()
		summary = f"グローバルIPアドレス: {data.get('ip')}"
		return render_page(
			"ipify.html",
			page_key="ipify",
			page_title="IPify API",
			summary=summary,
			result=data,
			result_json=json.dumps(data, ensure_ascii=False, indent=2),
		)
	except Exception as exc:  # noqa: BLE001
		return render_page(
			"ipify.html",
			page_key="ipify",
			page_title="IPify API",
			error=str(exc),
		)


@app.get("/iss-location")
def iss_location():
	try:
		data = get_iss_location()
		position = data.get("iss_position", {})
		summary = f"ISSの現在位置: 緯度 {position.get('latitude')} / 経度 {position.get('longitude')}"
		return render_page(
			"iss_location.html",
			page_key="iss-location",
			page_title="Open Notify API (ISS)",
			summary=summary,
			result=data,
			result_json=json.dumps(data, ensure_ascii=False, indent=2),
		)
	except Exception as exc:  # noqa: BLE001
		return render_page(
			"iss_location.html",
			page_key="iss-location",
			page_title="Open Notify API (ISS)",
			error=str(exc),
		)


@app.get("/astronauts")
def astronauts():
	try:
		data = get_astronauts()
		summary = f"現在宇宙に{data.get('number', 0)}人の宇宙飛行士が滞在しています。"
		return render_page(
			"astronauts.html",
			page_key="astronauts",
			page_title="Open Notify Astronaut API",
			summary=summary,
			result=data,
			result_json=json.dumps(data, ensure_ascii=False, indent=2),
		)
	except Exception as exc:  # noqa: BLE001
		return render_page(
			"astronauts.html",
			page_key="astronauts",
			page_title="Open Notify Astronaut API",
			error=str(exc),
		)


@app.get("/httpbin")
def httpbin():
	try:
		data = get_request_info()
		summary = f"リクエスト元IP: {data.get('origin')}"
		return render_page(
			"httpbin.html",
			page_key="httpbin",
			page_title="HTTPBin API",
			summary=summary,
			result=data,
			result_json=json.dumps(data, ensure_ascii=False, indent=2),
		)
	except Exception as exc:  # noqa: BLE001
		return render_page(
			"httpbin.html",
			page_key="httpbin",
			page_title="HTTPBin API",
			error=str(exc),
		)


@app.get("/fake-store")
def fake_store():
	limit = request.args.get("limit", "5").strip() or "5"
	try:
		limit_value = max(1, int(limit))
		data = get_products(limit_value)
		summary = f"商品を{len(data)}件取得しました。"
		return render_page(
			"fake_store.html",
			page_key="fake-store",
			page_title="Fake Store API",
			selected_limit=str(limit_value),
			summary=summary,
			result=data,
			result_json=json.dumps(data, ensure_ascii=False, indent=2),
		)
	except Exception as exc:  # noqa: BLE001
		return render_page(
			"fake_store.html",
			page_key="fake-store",
			page_title="Fake Store API",
			selected_limit=limit,
			error=str(exc),
		)


@app.get("/countries-now")
def countries_now():
	try:
		data = get_all_countries()
		countries = data.get("data", [])
		summary = f"{len(countries)}か国の都市情報を取得しました。"
		return render_page(
			"countries_now.html",
			page_key="countries-now",
			page_title="Countries Now API",
			summary=summary,
			result=countries[:20],
			result_json=json.dumps(countries[:20], ensure_ascii=False, indent=2),
		)
	except Exception as exc:  # noqa: BLE001
		return render_page(
			"countries_now.html",
			page_key="countries-now",
			page_title="Countries Now API",
			error=str(exc),
		)


@app.get("/deck-of-cards")
def deck_of_cards():
	deck_count = request.args.get("deck_count", "1").strip() or "1"
	try:
		deck_count_value = max(1, int(deck_count))
		data = shuffle_new_deck(deck_count_value)
		summary = f"{data.get('remaining')}枚のカードを含む新しいデッキを作成しました。"
		return render_page(
			"deck_of_cards.html",
			page_key="deck-of-cards",
			page_title="Deck of Cards API",
			selected_deck_count=str(deck_count_value),
			summary=summary,
			result=data,
			result_json=json.dumps(data, ensure_ascii=False, indent=2),
		)
	except Exception as exc:  # noqa: BLE001
		return render_page(
			"deck_of_cards.html",
			page_key="deck-of-cards",
			page_title="Deck of Cards API",
			selected_deck_count=deck_count,
			error=str(exc),
		)


@app.get("/chuck-norris")
def chuck_norris():
	try:
		data = get_chuck_norris_joke()
		summary = data.get("value", "ジョークを取得しました。")
		return render_page(
			"chuck_norris.html",
			page_key="chuck-norris",
			page_title="Chuck Norris API",
			summary=summary,
			result=data,
			result_json=json.dumps(data, ensure_ascii=False, indent=2),
		)
	except Exception as exc:  # noqa: BLE001
		return render_page(
			"chuck_norris.html",
			page_key="chuck-norris",
			page_title="Chuck Norris API",
			error=str(exc),
		)


if __name__ == "__main__":
	app.run(host="127.0.0.1", port=5000, debug=True)
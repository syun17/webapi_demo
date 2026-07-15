from api_client import ApiClient, fetch_json
from country_api import CountryApi, get_country, get_country_name_options
from dad_joke_api import DadJokeApi, get_joke
from json_placeholder_api import JsonPlaceholderApi, get_post, get_post_id_options
from picsum_api import PicsumApi, get_picsum_url
from pokemon_api import PokemonApi, get_pokemon, get_pokemon_name_options
from random_user_api import RandomUserApi, get_random_user
from quote_api import QuoteApi, get_quote
from weather_api import DEFAULT_WEATHER_AREA_CODE, WeatherApi, get_weather, get_weather_area_options
from fbi_wanted_api import FbiWantedApi, get_wanted_list
from agify_api import AgifyApi, get_age_prediction
from official_joke_api import OfficialJokeApi, get_random_joke as get_official_random_joke
from zipcloud_api import ZipcloudApi, get_address as get_zipcloud_address
from nominatim_api import NominatimApi, search_location
from ui_avatars_api import UiAvatarsApi, get_avatar_url
from bored_api import BoredApi, get_activity
from datamuse_api import DatamuseApi, get_related_words
from university_api import UniversityApi, search_universities
from zippopotamus_api import ZippopotamusApi, get_postal_info
from ipify_api import IpifyApi, get_public_ip
from iss_location_api import IssLocationApi, get_iss_location
from astronauts_api import AstronautsApi, get_astronauts
from httpbin_api import HttpbinApi, get_request_info
from fake_store_api import FakeStoreApi, get_products
from countries_now_api import CountriesNowApi, get_all_countries
from deck_of_cards_api import DeckOfCardsApi, shuffle_new_deck
from chuck_norris_api import ChuckNorrisApi, get_random_joke as get_chuck_norris_joke
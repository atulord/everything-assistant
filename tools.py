from typing import Annotated
from dotenv import load_dotenv
import requests
from requests.structures import CaseInsensitiveDict
from user_data import spotify
import os
from user_data import spotify, social_media

from utils import save_json

load_dotenv()
geocoding_api_key = os.getenv('GEOCODING_API_KEY')


def publish_tweet(tweet: Annotated[str, "content of tweet"]) -> dict:
    """
    Creates a tweet based on the users interests and personality. Should have a similar tone and content to the user's existing tweets.
    """
    social_media["twitter"]["recent_posts"].append(tweet)
    save_json(social_media, "./data/social_media.json")
    return {"tweet": tweet}


def send_message_to_contact(contact: Annotated[dict, "The name and information of the contact"], message: Annotated[str, "The message to send them"]):
    """
    Send a message to one of the user's contacts in order to keep in touch. Only message someone who currently exists in the users phone
    """
    return contact


def choose_song_from_playlist(playlist_name: Annotated[str, "Name of the playlist to select a song from"]) -> dict | None:
    """
    Selects a song from an existing playlist for the user. The name of the playlist has to already exist.
    """
    chosen_playlist = next(
        (playlist for playlist in spotify["playlists"] if playlist["name"] == playlist_name), None)
    return chosen_playlist


def create_new_playlist(playlist_name: Annotated[str, "Name of the playlist to create. Must be different from existing playlists"], songs: Annotated[list, "A list of songs to add to the playlist. They must match the theme of the playlist. Each songs should be in the format of SONG - ARTIST"]) -> dict | None:
    """
    Generate a new playlist based on the taste of the user. The name of the playlist must be unique and also in line with the users lifestyle.
    """
    spotify["playlists"].append({"name": playlist_name, "tracks": songs})
    save_json(spotify, "./data/spotify_playlists.json")
    return {"playlist": {"name": playlist_name, "tracks": songs}}


def get_address_from_geoapify(lat_long: list[float]) -> str | None:
    try:

        url = f"https://api.geoapify.com/v1/geocode/reverse?lat={lat_long[0]}&lon={lat_long[1]}&apiKey={geocoding_api_key}"

        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"

        resp = requests.get(url, headers=headers)
        return resp.json()["features"][0]["properties"]["formatted"]
    except Exception as e:
        print("We had an issue fetching your location.")
        return f"latitude {lat_long[0]} longitude {lat_long[1]}"


def get_route(start: Annotated[list, "Starting location for the route. Contains the latitude and longitude"], end: Annotated[list, "Ending location for the route. Contains the latitude and longitude"]) -> dict:
    """
    Fetches the recommended route for the given start and end locations. 
    """
    formatted_start_address = get_address_from_geoapify(start)
    formatted_end_address = get_address_from_geoapify(end)
    return {
        "start_location": formatted_start_address,
        "end_location": formatted_end_address
    }


tools = [get_route, publish_tweet,
         choose_song_from_playlist, send_message_to_contact, create_new_playlist]

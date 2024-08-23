from utils import load_csv, load_json

social_media = load_json('./data/social_media.json')
spotify = load_json('./data/spotify_playlists.json')
user_profile = load_json('./data/user_profile.json')
location_data = load_csv("./data/location.csv")
calendar_data = load_csv("./data/calendar.csv")
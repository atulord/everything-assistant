import pytest
from unittest.mock import patch, Mock
from tools import publish_tweet, send_message_to_contact, choose_song_from_playlist, create_new_playlist, get_route


def test_publish_tweet():
    tweet = "This is a test tweet"
    result = publish_tweet(tweet)
    assert result == {"tweet": tweet}
    # You might want to check if the tweet was added to social_media["twitter"]["recent_posts"]


def test_send_message_to_contact():
    contact = {"name": "John Doe", "phone": "1234567890"}
    message = "Hello, John!"
    result = send_message_to_contact(contact, message)
    assert result == contact


def test_choose_song_from_playlist():
    with patch('tools.spotify', {"playlists": [{"name": "Test Playlist", "tracks": ["Song1", "Song2"]}]}):
        result = choose_song_from_playlist("Test Playlist")
        assert result == {"name": "Test Playlist",
                          "tracks": ["Song1", "Song2"]}

    with patch('tools.spotify', {"playlists": []}):
        result = choose_song_from_playlist("Non-existent Playlist")
        assert result is None


@patch('tools.save_json')
def test_create_new_playlist(mock_save_json):
    playlist_name = "New Playlist"
    songs = ["Song1 - Artist1", "Song2 - Artist2"]
    result = create_new_playlist(playlist_name, songs)
    assert result == {"playlist": {"name": playlist_name, "tracks": songs}}
    mock_save_json.assert_called_once()


@patch('tools.requests.get')
@patch('tools.get_address_from_geoapify')
def test_get_route(mock_get_address, mock_get):
    mock_get_address.side_effect = ["Start Address", "End Address"]

    start = [40.7128, -74.0060]  # New York City coordinates
    end = [34.0522, -118.2437]  # Los Angeles coordinates

    result = get_route(start, end)

    assert result == {
        "start_location": "Start Address",
        "end_location": "End Address"
    }

    mock_get_address.assert_any_call(start)
    mock_get_address.assert_any_call(end)

# You might want to add a test for get_address_from_geoapify as well


@patch('tools.requests.get')
def test_get_address_from_geoapify(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {
        "features": [{"properties": {"formatted": "123 Test St, Test City, Test Country"}}]
    }
    mock_get.return_value = mock_response

    from tools import get_address_from_geoapify
    result = get_address_from_geoapify([40.7128, -74.0060])
    assert result == "123 Test St, Test City, Test Country"

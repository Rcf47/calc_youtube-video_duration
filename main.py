import os
import requests
import isodate
from dotenv import load_dotenv
from internal.app.extract_playlist_id import extract_playlist_id_from_file
from internal.app.get_playlist_id_from_url import get_playlist_id_from_url, save_playlist_id_to_file
from internal.app.check_cache import check_cache

load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")


def get_playlist_videos(api_key, playlist_id):
    url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=contentDetails&playlistId={playlist_id}&key={api_key}&maxResults=50"
    videos = []

    while url:
        response = requests.get(url)
        data = response.json()

        videos.extend(item ["contentDetails"]["videoId"] for item in
                      data.get("items", []))
        
        next_page_token = data.get("nextPageToken")
        url = f'https://www.googleapis.com/youtube/v3/playlistItems?part=contentDetails&playlistId={playlist_id}&key={api_key}&maxResults=50&pageToken={next_page_token}' if next_page_token else None

    return videos


def get_video_duration(api_key, video_id):
    url = f'https://www.googleapis.com/youtube/v3/videos?id={video_id}&part=contentDetails&key={api_key}'
    response = requests.get(url)
    data = response.json()

    if data["items"]:
        duration = data["items"][0]["contentDetails"]["duration"]
        return isodate.parse_duration(duration).total_seconds()
    
    return 0


def main():
    url = input("Enter YouTube playlist URL: ")
    
    if check_cache(url):
        print(check_cache(url))
        return
        
    playlistid = get_playlist_id_from_url(url)
    save_playlist_id_to_file(playlistid, url)

    PLAYLIST_ID = extract_playlist_id_from_file()
    video_ids = get_playlist_videos(API_KEY, PLAYLIST_ID)

    total_duration = sum(get_video_duration(API_KEY, video_id) for video_id in video_ids)
    
    hours, remainder = divmod(total_duration, 3600)
    minutes, seconds = divmod(remainder, 60)

    string_for_cache = f'Общее время просмотра плейлиста: {int(hours)} часов, {int(minutes)} минут, {int(seconds)} секунд.'
    print(string_for_cache)

    with open("data/time_cache.txt", "a") as file:
        file.write(url + ": " + string_for_cache + "\n")

if __name__ == "__main__":
    main()

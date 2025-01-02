from urllib.parse import urlparse, parse_qs


def get_playlist_id_from_url(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    
    return query_params.get('list', [None])[0]


def save_playlist_id_to_file(playlist_id, url, filename="data/playlist_id.txt"):
    with open(filename, "a") as file:
        file.write(url + ": " + playlist_id + "\n")


def main(url):
    playlist_id = get_playlist_id_from_url(url)
    
    if playlist_id:
        save_playlist_id_to_file(playlist_id, url)
        print(f"Playlist ID saved: {playlist_id}")
    else:
        print("Invalid YouTube playlist URL")

if __name__ == "__main__":
    url = input("Enter YouTube playlist URL: ")
    main(url)

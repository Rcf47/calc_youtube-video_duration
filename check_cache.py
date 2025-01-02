def check_cache(url):
    with open("time_cache.txt", "r") as file:
        for line in file:
            if url in line:
                return line.strip()
    return False

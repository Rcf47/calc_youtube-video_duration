def extract_playlist_id_from_file(filename='playlist_id.txt'):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()  # Читаем все строки файла
            last_line = lines[-1] if lines else None  # Получаем последнюю строку

            if last_line:
                # Разделяем строку по двоеточию и берем первую часть
                playlist_id = last_line.split(': ')[1].strip()
                return playlist_id
            else:
                print("Файл пуст.")
                return None
    except FileNotFoundError:
        print(f"Файл {filename} не найден.")
        return None


if __name__ == '__main__':
    playlist_id = extract_playlist_id_from_file()
    print(playlist_id)

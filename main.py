import vlc
from yandex_music import Client
from yandex_music import SimilarTracks
import requests
import dotenv
import os

dotenv.load_dotenv()
API_KEY = os.getenv("API_KEY")
client = Client(API_KEY).init()


def search_request(query):
    search_result = client.search(query)
    track_results = []
    if search_result.tracks:
        track_results = search_result.tracks.results[:5]
    return track_results


def print_result(track_results, query):
    text = [f'Результаты по запросу "{query}":', '']
    if track_results:
        text.append('❗️Лучшие треки:')
        for idx, track in enumerate(track_results, 1):
            artists = ' - ' + ', '.join(artist.name for artist in track.artists) if track.artists else ''
            text.append(f'{idx}. {track.title} {artists}')
    text.append('')
    print('\n'.join(text))


def player_music(list_of_tracks):
    num = int(input('Какой бы трек вы хотел воспроизвести?\nНажмите 0, чтобы начать поиск заново\n')) - 1
    while num == -1:
        input_query = input('Введите поисковой запрос: ')
        a = search_request(input_query)
        print_result(a, input_query)
        player_music(a)
    list_of_tracks[num].download(f'{list_of_tracks[num].title}.mp3') # а если трек уже скачан?
    player = vlc.MediaPlayer(f'{list_of_tracks[num].title}.mp3')
    player.play()
    while True:
        text = input("Если понадобится, то напишите команды\n")
        if text == "play":
            player.play()
        elif text == "pause":
            player.pause()


if __name__ == '__main__':
    while True:
        input_query = input('Введите поисковой запрос: ')
        a = search_request(input_query)
        print_result(a, input_query)
        player_music(a)

from aiogram.types import file
from bs4 import BeautifulSoup as BS
from pytube import YouTube
import requests
import re

from requests.api import request
from config import API_KEY, MUSIC_ROOT

headers = {
    'User-agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582'
}


class Youtube:
    YOUTUBE_SEARCH_LINK = "https://www.youtube.com/results?search_query="
    YOUTUBE_LINK = "https://www.youtube.com/watch?v=" 

    def __init__(self, user_request) -> None:
        self.request = user_request


    def find_url(self):
        """Finds the link to a video"""
        html_content = requests.get(self.YOUTUBE_SEARCH_LINK + "+".join(self.request.split()), headers=headers)
        search_results = re.search(r"watch\?v=(\S{11})", html_content.text)
        return self.YOUTUBE_LINK + str(search_results[0])


    @staticmethod
    def download_audio(link):
        """Downloads audio of yotube video and returns the path to it"""
        return YouTube(link).streams.filter(only_audio=True).first().download(output_path=MUSIC_ROOT)


class Azlyr:
    AZ_SEARCH_LINK = 'https://search.azlyrics.com/search.php?q='

    def __init__(self, user_request) -> None:
        self.request = user_request

    def get_link(self):
        self.link = self.AZ_SEARCH_LINK + "+".join(self.request.split(' '))

    def get_song_info(self):
        response = requests.get(self.link, headers=headers)
        html_content = BS(response.text, "lxml")
        rezult_panel = html_content.find('td', class_="text-left visitedlyr")
        if not rezult_panel:
            return None
        song_name = " - ".join(i.text.strip() for i in rezult_panel.find_all('b')[:2])
        return song_name


class Shazam:
    AUDD_API_LINK ='https://api.audd.io/'


    def __init__(self, file_path) -> None:
        self.file = file_path

    def find_song_info(self):
        with open(self.file, 'rb') as f:
            data = {
                'api_token': API_KEY,
                'return': 'spotify',
            }
            files = {
                'file': f,
            }
            result = requests.post(self.AUDD_API_LINK, data=data, files=files).json()
        if result["status"] == "success" and result["result"]:
            return result["result"]["artist"] +' - '+ result["result"]["title"]
        return None

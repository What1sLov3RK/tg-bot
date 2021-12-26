from pytube import YouTube
import requests
import re
from config import API_KEY, PATH
from bs4 import BeautifulSoup as BS




from requests.models import Response


class youtube:
	def __init__(self, request: str = None) -> None:
		if request[:31] != "https://www.youtube.com/watch?v=":
			request = self.__createlink(request)
		self.link = request


	def __createlink(self, keywords):
		html_content = requests.get("https://www.youtube.com/results?search_query=" + "+".join(keywords.split()))
		search_results = re.search(r"watch\?v=(\S{11})", html_content.read().decode())
		return "https://www.youtube.com/" + str(search_results[0])


	def download_audio(self):
		"""Returns path to downloaded file"""
		return YouTube(self.link).streams.filter(only_audio=True).first().download(output_path=PATH + r'\music')


class AzLyr:
	SEARCH_LINK = "https://search.azlyrics.com/search.php?q="

	def __init__(self, request: str = None) -> None:
		self.request = request

	def define_song(self):
		response = requests.get(self.SEARCH_LINK + "+".join(self.request.split()))
		html_content = BS(response.text, "lxml")
		rezult_panel = html_content.find('td', class_="text-left visitedlyr")
		if not rezult_panel:
			return None
		song_name = " - ".join(i.text.strip() for i in rezult_panel.find_all('b')[:2])
		return song_name
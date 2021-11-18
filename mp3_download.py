from pytube import YouTube 
import urllib.request
import urllib.parse
import re
import os
from validators import url

class Music:
	def downloader(self, string):
		"""Downloads an mp3 audio of Youtube video
		
		`string` can be both url or video name

		returns path to downloaded file
		"""
		if not url(string):
			string = self.__find_url_by_name(string)
		return self.__mp3_from_youtube_url(string)
	

	def __mp3_from_youtube_url(self, url:str):
		return YouTube(url).streams.filter(only_audio=True).first().download(output_path=os.getcwd() + r'\music', filename="aboba.mp3")

	def __find_url_by_name(self, video_name:str):
		html_content = urllib.request.urlopen("http://www.youtube.com/results?search_query=" +  urllib.parse.quote(video_name.replace(" ","+"),encoding="utf8"))
		search_results = re.search(r"watch\?v=(\S{11})", html_content.read().decode())
		return "http://www.youtube.com/watch?v="+str(search_results[0])
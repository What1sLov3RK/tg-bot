from pytube import YouTube 
import urllib.request
import urllib.parse
import re
import os
import validators

class Music:
	def downloader(self, string):
		"""Downloads an mp3 audio of Youtube video
		
		`string` can be both url or video name

		returns path to downloaded file
		"""
		if validators.url(string):
			return self.__mp3_from_youtube_url(string)
		else:
			return self.__mp3_from_youtube_name(string)


	def __mp3_from_youtube_url(self, url:str):
		return YouTube(url).streams.filter(only_audio=True).first().download(output_path=os.getcwd() + r'\music', filename="aboba.mp3")

	def __mp3_from_youtube_name(self, video_name:str):
		html_content = urllib.request.urlopen("http://www.youtube.com/results?search_query=" +  urllib.parse.quote(video_name.replace(" ","+"),encoding="utf8"))
		search_results = re.search(r"watch\?v=(\S{11})", html_content.read().decode())
		self.__mp3_from_youtube_url("http://www.youtube.com/watch?v="+str(search_results[0]))
from bs4 import BeautifulSoup as BS
from pytube import YouTube
import requests
import re
from config import API_KEY, MUSIC_ROOT


def youtube_search(request):
    html_content = requests.get("https://www.youtube.com/results?search_query=" + "+".join(request.split()), headers = {'User-agent': 'Reaper bot 1.1'})
    search_results = re.search(r"watch\?v=(\S{11})", html_content.text)
    return "https://www.youtube.com/" + str(search_results[0])


def youtube_download(link):
    return YouTube(link).streams.filter(only_audio=True).first().download(output_path=MUSIC_ROOT)
     

def lyrics_search(request:str):
    response = requests.get('https://search.azlyrics.com/search.php?q=' + "+".join(request.split(' ')))
    print(response.text)
    html_content = BS(response.text, "lxml")
    rezult_panel = html_content.find('td', class_="text-left visitedlyr")
    print(rezult_panel)
    if not rezult_panel:
        return None
    song_name = " - ".join(i.text.strip() for i in rezult_panel.find_all('b')[:2])
    return song_name


def shazam_audio(file_name):
	data = {
		'api_token': API_KEY,
		'return': 'spotify',
	}
	files = {
		'file': open(file_name, 'rb'),
	}
	result = requests.post('https://api.audd.io/', data=data, files=files).json()
	if result["status"] == "success" and result["result"]:
		return result["result"]["artist"] +' - '+ result["result"]["title"]
	return None
	
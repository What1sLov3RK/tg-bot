import urllib.request
import urllib.parse
import re
from pytube import YouTube
import os
import requests
import os
from config import API_KEY


def youtube_search(request):
    html_content = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + urllib.parse.quote(request.replace(" ", "+"),encoding="utf8"))
    search_results = re.search(r"watch\?v=(\S{11})", html_content.read().decode())
    return "https://www.youtube.com/" + str(search_results[0])


def youtube_download(link):
    return YouTube(link).streams.filter(only_audio=True).first().download(output_path=os.getcwd() + r'\music')
     

def lyrics_search(request):
    html_content = urllib.request.urlopen("https://search.azlyrics.com/search.php?q=" + urllib.parse.quote(request.replace(" ", "+"),encoding="utf8"))
    search_results = re.findall(r'https://www.azlyrics.com/lyrics/[\w\.-]+/+\w+.+html', html_content.read().decode())
    if not search_results:
        return None
    name = re.search(r'https://www.azlyrics.com/lyrics/([\w.-]+)/([\w.-]+)', search_results[0])  
    name=name.group(1)
    song_url = urllib.request.urlopen(search_results[0])
    song_name_url= re.search(r'(<b>")[^"]*("</b>)',song_url.read().decode())
    return song_name_url.group(0).strip("<b>/")


def shazam_audio(file_name):
	data = {
		'api_token': API_KEY,
		'return': 'spotify',
	}
	files = {
		'file': open(os.getcwd()+'/voice/' + file_name, 'rb'),
	}
	result = requests.post('https://api.audd.io/', data=data, files=files).json()
	if result["status"] == "success" and result["result"]:
		return result["result"]["artist"] +' - '+ result["result"]["title"]
	return "Song not found"
	
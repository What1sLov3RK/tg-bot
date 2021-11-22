import requests
import os
from config import API_KEY
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
	
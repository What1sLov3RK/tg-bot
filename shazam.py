import requests
import os
def shazam(file_name):
	data = {
		'api_token': 'd7cf75af52de7e0b9c6ae5b2751a42be',
		'return': 'spotify',
	}
	files = {
		'file': open(os.getcwd()+'/audio_to_shazam/' + file_name, 'rb'),
	}
	result = requests.post('https://api.audd.io/', data=data, files=files)
	return result.json()["result"]["artist"] +' - '+ result.json()["result"]["title"]
	
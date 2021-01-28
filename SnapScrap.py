#!/usr/bin/python3

from bs4 import BeautifulSoup
from time import sleep
import requests
import urllib
import json
import os

query = input("Username bitte eintippen: ")

path = query
try:
	os.mkdir(path)
except FileExistsError:
	print("This user has a folder in your System.")

os.chdir(path)

url = "https://story.snapchat.com/u/"

mix = url + str(query)
print(mix)

r = requests.get(mix)

if r.ok:
	print("\033[1;32;40m Snapchat site is Responding :)  \n")
	
else:
	print("\033[31m Snap! No connection with Snap! \n Verbindung war nicht erfolgreich!")
	
soup = BeautifulSoup(r.content, "html.parser")

snaps = soup.find_all("script")[4].string.strip()

print("The script exists. \n")

data = json.loads(snaps)

#displayUsername = data["props"]["userDisplayInfo"]["username"]
#print("Du hast nach", displayUsername, "gesucht. \n")

try:
	for i in data["props"]["story"]["snapList"]:
		file_url = (i["snapUrls"]["mediaUrl"])
		file_name = file_url.split('/')[-3]
		
		print(file_url)
		
		r = requests.get(file_url, stream=True)

		if r.status_code == 200:
			with open(file_name, 'wb') as f:
				for chunk in r:
					f.write(chunk)
				print(f"\033[33mGetting posts of:\033[33m {query}")
		else:
			print("Cannot make connection to download image")
		
except KeyError:
	print("This user has no Story in the last 24h. \n Dieser nutzer hat keine Storys in letzen 24h.")
else:
	print("\nAt least one Story found. Successfully Downloaded. \n Mindestns ein Story gefunden. Erfolgreich heruntergeladen.")

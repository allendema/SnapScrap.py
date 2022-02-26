#!/usr/bin/python3

from bs4 import BeautifulSoup
from time import sleep
import requests
import json
import sys
import os

query = input("Enter a username: ")
path = query

try:
	os.mkdir(path)
except FileExistsError:
	print("This user has a folder in your System.")

os.chdir(path)

url = "https://story.snapchat.com/@"

mix = url + str(query)
print(mix)

headers = {
	'User-Agent': '"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0',
}

r = requests.get(mix, headers=headers)

if r.ok:
	print("\033[1;32;40m Snapchat site is Responding :)  \n")

else:
	print("\033[31m Snap! No connection with Snap!")
	sys.exit(1)

soup = BeautifulSoup(r.content, "html.parser")
#print(soup)

snaps = soup.find(id="__NEXT_DATA__").string.strip()


print("The script exists. \n")

data = json.loads(snaps)

try:
	bitmoji = data["props"]["pageProps"]["userProfile"]["publicProfileInfo"]["snapcodeImageUrl"]
	bio = data["props"]["pageProps"]["userProfile"]["publicProfileInfo"]["bio"]

except KeyError:
	bitmoji = data["props"]["pageProps"]["userProfile"]["userInfo"]["snapcodeImageUrl"]
	bio = data["props"]["pageProps"]["userProfile"]["userInfo"]["displayName"]
	print("Here is the Bio:\n", bio, "\nand Bitmoji:\n", bitmoji)
	print("\nThis user is private.")
	sys.exit(1)

print("Bio of the user:\n", bio)
print("\nHere is the Bitmoji:\n", bitmoji)


print(f"\n\033[33mGetting posts of:\033[33m {query}\n")

try:
	# Find all links with a for-loop
	for i in data["props"]["pageProps"]["story"]["snapList"]:

		file_url = i["snapUrls"]["mediaUrl"]

		if file_url == "":
			print("There is a Story but no URL is provided by Snapchat.")
			continue

		# Download media and use a short unique file_name
		r = requests.get(file_url, stream=True, headers=headers)

		if "image" in r.headers['Content-Type']:
			file_name = r.headers['ETag'].replace('"', '') + ".jpeg"
			print(file_name)			

		elif "video" in r.headers['Content-Type']:
			file_name = r.headers['ETag'].replace('"', '') + ".mp4"
			print(file_name)

		#  Check if this file / file_name exists
		if os.path.isfile(file_name) :
			continue
	
		#  Sleep a bit
		sleep(0.3)	

		if r.status_code == 200:
			with open(file_name, 'wb') as f:
				for chunk in r:
					f.write(chunk)

		else:
			print("Cannot make connection to download media!")

except KeyError:
	print("No user stories found for the last 24h.")
else:
	print("\nAt least one Story found. Successfully Downloaded.")

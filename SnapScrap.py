#!/usr/bin/python3
__author__ = "https://codeberg.org/allendema"

from time import sleep
import time
import json
import sys
import os

from bs4 import BeautifulSoup
import requests


def user_input():
	"""Check for username argument
	Otherwise get it from user input"""

	try:
		username = sys.argv[1]
	except Exception:
		username = input("Enter a username: ")

	path = username

	if os.path.exists(path):
		print("This user has a folder in your System.")

	else:
		os.mkdir(path)

	os.chdir(path)

	return username


YELLOW = "\033[1;32;40m"
RED = "\033[31m"

headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/103.0.2'}

base_url = "https://story.snapchat.com/@"
username = user_input()

mix = base_url + username
print(mix)


def get_json():
	"""Get json from the website"""

	r = requests.get(mix, headers=headers)

	if r.ok:
		#print(f"{YELLOW} Snapchat site is Responding :)  \n")
		pass

	else:
		sys.exit(f"{RED} Oh Snap! No connection with Snap!")

	soup = BeautifulSoup(r.content, "html.parser")

	# Find the script with the JSON data on the site
	snaps = soup.find(id="__NEXT_DATA__").string.strip()

	#print("The script exists. \n")
	data = json.loads(snaps)

	return data


def profile_metadata(json_dict=get_json()):
	"""Detect public profile, then print bio and bitmoji"""
	# if public
	try:
		bitmoji = json_dict["props"]["pageProps"]["userProfile"]["publicProfileInfo"]["snapcodeImageUrl"]
		bio = json_dict["props"]["pageProps"]["userProfile"]["publicProfileInfo"]["bio"]

	# if not public
	except KeyError:
		bitmoji = json_dict["props"]["pageProps"]["userProfile"]["userInfo"]["snapcodeImageUrl"]
		bio = json_dict["props"]["pageProps"]["userProfile"]["userInfo"]["displayName"]

		print(f"{YELLOW}Here is the Bio: \n {bio}\n")
		print(f"Bitmoji:\n {bitmoji}\n")
		print(f"{RED} This user is private.")

		sys.exit(1)

	print(f"{YELLOW}\nBio of the user:\n", bio)
	print(f"\nHere is the Bitmoji:\n {bitmoji} \n")

	print(f"Getting posts of: {username}\n")


def download_media(json_dict=get_json()):
	"""Print media URLs and download media."""

	try:
		# Get all links with a for-loop
		for i in json_dict["props"]["pageProps"]["story"]["snapList"]:

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
			if os.path.isfile(file_name):
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
		print(f"{RED}No user stories found for the last 24h.")
	else:
		print("\nAt least one Story found. Successfully Downloaded.")


def main():
	start = time.perf_counter()

	profile_metadata()
	download_media()

	end = time.perf_counter()
	total = end - start

	print(f"\n\nTotal time: {total}")


if __name__ == "__main__":
	main()

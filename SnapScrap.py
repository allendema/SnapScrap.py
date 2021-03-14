#!/usr/bin/python3

from bs4 import BeautifulSoup
import requests
import json
import os

query = input("Enter a username: ")

path = query

try:
    os.mkdir(path)
except FileExistsError:
    print("This user has a folder in your System.")

os.chdir(path)

url = "https://story.snapchat.com/u/"

mix = url + str(query)
print(mix)

headers = {
    'User-Agent': '"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0',
}

r = requests.get(mix, headers = headers)

if r.ok:
    print("\033[1;32;40m Snapchat site is Responding :)  \n")
    
else:
    print("\033[31m Snap! No connection with Snap!")
    
soup = BeautifulSoup(r.content, "html.parser")

snaps = soup.find_all("script")[4].string.strip()

print("The script exists. \n")

data = json.loads(snaps)

#displayUsername = data["props"]["userDisplayInfo"]["username"]
#print("You have searched for", displayUsername, \n")

bitmoji = data["props"]["pageLinks"]["snapcodeImageUrl"]
#print("Here is the Bitmoji: ", bitmoji)

try:
    for i in data["props"]["story"]["snapList"]:

        file_url = (i["snapUrls"]["mediaUrl"])
        #file_name = file_url.split('/')[-3][:7]
        splitted_name = file_url.split('/')[-3][:7]
        
        mp4 = file_url.rfind("mp4")
        jpg = file_url.rfind("jpg")
        png = file_url.rfind("png")
        
        if mp4 != -1:
            #print("We have mp4 here.")
            file_name = splitted_name + ".mp4"
        if jpg != -1:
            #print("We have jpg here.")
            file_name = splitted_name + ".jpg"
        if png != -1:
            #print("We have png here.")
            file_name = splitted_name + ".png"
        

        print(file_url)
        
        r = requests.get(file_url, stream=True, headers = headers)

        if r.status_code == 200:
            with open(file_name, 'wb') as f:
                for chunk in r:
                    f.write(chunk)
                print(f"\033[33mGetting posts of:\033[33m {query}")
        else:
            print("Cannot make connection to download media!")
        
except KeyError:
    print("This user has no Story in the last 24h.")
else:
    print("\nAt least one Story found. Successfully Downloaded.")


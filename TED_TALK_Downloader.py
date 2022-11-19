"""
This Program is any kind of download video from ted talk website
Usage:  python3 TED_TALK_Downloader.py https://ted.com/talk/aljkflakjfl.mp4
        python3 TED_TALK_Downloader.py <URL>
        
#### If this program create error when download video content from web, Sorry for that. ####
"""



import requests
from bs4 import BeautifulSoup
import re
import sys


if len(sys.argv) > 1:
    url = sys.argv[1]
    page = requests.get(url)
else:
    print('Please enter the TED TALK VIDEO URL.')
    quit()
# getting source from url
soup = BeautifulSoup(page.content, 'lxml')
script_video = soup.find_all('script', id='__NEXT_DATA__')
# getting the link of video
video_link = re.search(r'((https?:\/\/)\S+\.mp4)', str(script_video))
video_title = re.search(r'\"title\":\"([\S\s\,\-]+)\"\,\"socialTitle\"\:', str(script_video))
print(video_title.group(1), ':', video_link.group(1)) # printing the link and title of video
print('Download started...') 
# getting file download
print('File storing as a ' + video_title.group(1))
video = requests.get(video_link.group(1))
try:
    if '\"*:<>?/\\|' not in video_title.group(1):
        with open(video_title.group(1)+'.mp4', 'wb') as f:
            f.write(video.content)
    else:
    	with open('video.mp4', 'wb') as f:
        	f.write(video.content)
except:
    print('something went wrong')
    quit()
print('Download completed...')

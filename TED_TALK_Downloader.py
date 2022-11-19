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
video_title = re.search(
    r'\"title\":\"([\S\s\,\-]+)\"\,\"socialTitle\"\:', str(script_video))
print(video_title.group(1), ':', video_link.group(1))
print('Download started...')
# getting file download
video = requests.get(video_link.group(1))
print('File storing as a ' + video_title.group(1))
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

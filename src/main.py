import requests
import json
import re

API_KEY = 'SOME-API-KEY'
# playlistId = 'PL4o29bINVT4EG_y-k5jGoOu3-Am8Nvi10'
prefix = 'https://www.googleapis.com/youtube/v3'
videoList = []

playlistId = input('Enter playlist id ')

originalRequestForPlaylist = prefix + "/playlistItems" + '?part=contentDetails&playlistId=' + playlistId + '&maxResults=50&key=' + API_KEY
jsonResponse = requests.get(originalRequestForPlaylist).json()
isResponseProcessingPending = True

while isResponseProcessingPending:
    items = jsonResponse['items']
    for item in items:
        videoList.append(item['contentDetails']['videoId'])
    if not 'nextPageToken' in jsonResponse.keys():
        isResponseProcessingPending = False
        break
    nextPageToken = jsonResponse['nextPageToken']
    newRequest = originalRequestForPlaylist + '&pageToken=' + nextPageToken
    jsonResponse = requests.get(newRequest).json()

print('Total videos in playlist is ' + str(len(videoList)))

videoDuration = []

originalRequestForVideo = prefix + '/videos' + '?part=contentDetails' + '&key=' + API_KEY

for i in range(0, len(videoList), 50):
    requestForVideo = originalRequestForVideo
    for j in range(i, min(i+50, len(videoList)), 1):
        requestForVideo = requestForVideo + '&id=' + videoList[j]
    jsonResponse = requests.get(requestForVideo).json()
    items = jsonResponse['items']
    for item in items:
        videoDuration.append(item['contentDetails']['duration'])

hours = 0
minutes = 0
seconds = 0

for duration in videoDuration:
    h = 0
    m = 0
    s = 0
    if 'H' in duration:
        h = re.findall(r"(\d+)H", duration)[0]
    if 'M' in duration:
        m = re.findall(r"(\d+)M", duration)[0]
    if 'S' in duration:
        s = re.findall(r"(\d+)S", duration)[0]
    hours += int(h)
    minutes += int(m)
    seconds += int(s)

minutes += seconds//60
seconds %= 60
hours += minutes//60
minutes %= 60

print('Total time for watching playlist is ' + str(hours) + ' Hours ' + str(minutes) + ' Minutes ' + str(seconds) + ' Seconds')


# ==================================== #
#          youtube-downloader          #
# ==================================== #

# ------------ import libs ----------- #

import time # calculate script's run time
from datetime import datetime # generate timestamp for saving data
import os # create folders

import feedparser # read RSS
import yt_dlp # download YouTube videos # NOTE: https://github.com/ytdl-org/youtube-dl/issues/30102#issuecomment-943849906

# --------- start + run time --------- #

start_time = time.time() # run time start
print("Starting the script...") # status

# ----- timestamp for saving data ---- #

this_run_datetime = timestamp = datetime.strftime(datetime.now(), '%y%m%d-%H%M%S') # eg. 210120-173112

# ----- check and create folders ----- #

# files
# if not os.path.isdir("downloaded_videos"): # if folder doesn't exist
#     os.mkdir("downloaded_videos") # create folder 
#     print("Folder created: downloaded_videos") # status

# ---------- fun begins here --------- #

# ------------- read RSS ------------- #

RSSfeed = 'https://www.youtube.com/feeds/videos.xml?channel_id=UC8LJZNHnqXKg5TMgyvxszPA' 
print("Reading RSS feed...") # status

try:
    read_RSS = feedparser.parse(RSSfeed) # read the RSS feed
    # print(read_RSS.feed.link) # print channel URL 
    videoTitle = read_RSS.entries[0].title # get latest video's title
    print(f"Latest video's title: {videoTitle}") # print the latest video's URL
    videoURL = read_RSS.entries[0].link # get the latest video's URL
    print(f"Latest video's URL: {videoURL}") # print the latest video's URL
# except (IndexError): # Internet down, wrong URL
except: # Internet down, wrong URL
    print("Can't read RSS file. Check your internet connection and RSS feed's URL, then try again. Closing...") # status

# TODO: check which video was downloaded last and go from there
# print(read_RSS.entries[1].link) # get previous video's URL

# ---------- download video ---------- #

# TODO: exclude segments with SponsorBlock parameters

# downloadPath = '' # TODO: change

#  parameters for the downloader
ydl_opts = { 
    'quiet': True, # don't throw status messages in the console
    # 'outtmpl': downloadPath + r'/%(title)s.%(ext)s' # TODO: uncomment when line #55 changed 
    } 

try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(videoURL, download=False) # get info about the video without downloading
        # print("Getting video's title...") # status 
        # video_title = info_dict.get('title', None) # get video's title
        # print(f"Video's title: {video_title}") # print video's title
        print("Downloading the video...") # status
        ydl.download(videoURL) # now download the video
        print("Download complete.") # status
except: # Internet down, wrong URL
    print("Can't download the video. Check your internet connection and video's URL, then try again. Closing...") # status

# TODO: convert to .mp3?

# ----------- fun ends here ---------- #

# ------------- run time ------------- #

end_time = time.time() # run time end 
total_run_time = round(end_time-start_time,2)
print(f"Total script run time: {total_run_time} seconds.")
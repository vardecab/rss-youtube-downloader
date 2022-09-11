# ==================================== #
#          youtube-downloader          #
# ==================================== #

# ------------ import libs ----------- #

import time # calculate script's run time
from datetime import datetime # generate timestamp for saving data
import os # create folders

import yt_dlp # https://github.com/ytdl-org/youtube-dl/issues/30102#issuecomment-943849906

# --------- start + run time --------- #

start_time = time.time() # run time start
print("Starting the script...") # status

# ----- timestamp for saving data ---- #

this_run_datetime = timestamp = datetime.strftime(datetime.now(), '%y%m%d-%H%M%S') # eg. 210120-173112

# ----- check and create folders ----- #

# files
if not os.path.isdir("downloaded_videos"): # if folder doesn't exist
    os.mkdir("downloaded_videos") # create folder 
    print("Folder created: downloaded_videos") # status

# ---------- fun begins here --------- #

# TODO: look at RSS 

# ---------- download video ---------- #

# TODO: download video from YouTube 
    # TODO: exclude segments with SponsorBlock parameters  
videoURL = 'https://www.youtube.com/watch?v=J3-R9W_OnHY'
ydl_opts = {} # parameters for the downloader 
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info_dict = ydl.extract_info(videoURL, download=False) # get info about the video without downloading
    video_title = info_dict.get('title', None) # get video's title
    print(f"Tytuł: {video_title}") # print video's title
    ydl.download([videoURL]) # now download the video

# ----------- fun ends here ---------- #

# ------------- run time ------------- #

end_time = time.time() # run time end 
total_run_time = round(end_time-start_time,2)
print(f"Total script run time: {total_run_time} seconds.")
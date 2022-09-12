# ==================================== #
#        rss-youtube-downloader        #
# ==================================== #

# ------------ import libs ----------- #

# core ↓
import yt_dlp # download YouTube videos # NOTE: https://github.com/ytdl-org/youtube-dl/issues/30102#issuecomment-943849906
import feedparser # read RSS

# other ↓
import time # calculate script's run time
from datetime import datetime # generate timestamp for saving data
# import os # create folders

# notifications ↓ 
from sys import platform # check platform (Windows/macOS)
if platform == 'darwin':
    import pync # macOS notifications
elif platform == 'win32':
    from win10toast_click import ToastNotifier # Windows 10/11 notifications
    toaster = ToastNotifier() # initialize win10toast
    
iconDownload = "icons/download.png"
iconCheckmark = "icons/checkmark.png"

# import webbrowser # open URLs from notification

# NOTE: fix certificate issue -> https://stackoverflow.com/questions/28282797/feedparser-parse-ssl-certificate-verify-failed
if platform != 'win32': # check if user is using macOS
    import ssl
    if hasattr(ssl, '_create_unverified_context'):
        ssl._create_default_https_context = ssl._create_unverified_context

# --------- start + run time --------- #

start_time = time.time() # run time start
print("Starting the script...") # status

# ----- timestamp for saving data ---- #

# this_run_datetime = timestamp = datetime.strftime(datetime.now(), '%y%m%d-%H%M%S') # eg. 210120-173112

# ----- check and create folders ----- #

# files
# if not os.path.isdir("downloaded_videos"): # if folder doesn't exist
#     os.mkdir("downloaded_videos") # create folder 
#     print("Folder created: downloaded_videos") # status

# ---------- fun begins here --------- #

# ---------- download video ---------- #

# TODO: exclude segments with SponsorBlock parameters
# TODO: convert to .mp3?

def downloadVideo(videoURL):
    
    downloadPath = r'/Users/x/TV Shows/' # download location

    #  parameters for the downloader
    ydl_opts = { 
        'quiet': True, # don't throw status messages in the console
        'outtmpl': downloadPath + r'/%(title)s.%(ext)s' # download location + name of the file
        } 

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # info_dict = ydl.extract_info(videoURL, download=False) # get info (title, metadata, etc.) about the video without downloading
            
            print("Downloading the video...") # status
            ydl.download(videoURL) # now download the video
            print("Video downloaded or it's already on the disk.") # status
            # TODO: how to check if downloading or already on disk?
            
            # notifications 
            if platform == "darwin": # macOS
                pync.notify(
                    f"Video downloaded or already on the disk.",
                    title='rss-youtube-downloader',
                    contentImage=iconDownload,
                    sound=""
                    # open=
                    )
            elif platform == "win32": # Windows
                toaster.show_toast(
                    title="rss-youtube-downloader", 
                    msg=
                    f"Video downloaded or already on the disk.",
                    icon_path="icons/download.ico",
                    duration=None,
                    threaded=True
                    # callback_on_click=
                    ) # duration=None - leave notification in Notification Center; threaded=True - rest of the script will be allowed to be executed while the notification is still active
            
            with open('videos.txt','a') as saveFile: # create and save file with downloaded videos' URLs
                saveFile.write(videoURL + "\n")
                # NOTE: not very pretty but works
                    # TODO: avoid duplicates 

    except: # Internet down, wrong URL
        print(f"Can't download the video. Check your internet connection and video's URL ({videoURL}), then try again. Closing...") # status

# ------------- read RSS ------------- #

# TODO: get input + default on timeout 
# TODO: ask which feed to check, type 1/2/3/4/5 or name of the channel 
# TODO: check multiple feeds at once? function?

RSSfeed = 'https://www.youtube.com/feeds/videos.xml?channel_id=UC8LJZNHnqXKg5TMgyvxszPA' 
print("Reading RSS feed...") # status

try:
    read_RSS = feedparser.parse(RSSfeed) # read the RSS feed
except: 
    print(f"Can't read the RSS feed. Maybe there is a problem with your internet connection or with the `RSSfeed` URL: {RSSfeed}. Closing...")
    exit()

# - check to not duplicate downloads - #

try:
    with open('videos.txt', 'r') as openFile: # open file
        file_content = openFile.read() # read file
except: 
    with open('videos.txt', 'w') as openFile: # create a file
        print("There was a problem with reading the `videos.txt` file. It didn't exist so it was created now.")
    with open('videos.txt', 'r') as openFile: # open file
        file_content = openFile.read() # read file
    
counter = 1 # NOTE: how far back we should look for the videos (3 = 4 videos back, 10 = 11 videos back, 0 = just newest video)
# FIX: not working when eg. 2nd video downloaded and you're looking for the 1st and 3rd
try:
    if read_RSS.entries[counter].link in file_content:
        print(f"Newest video already watched or downloaded and available on the disk.")
         # notifications 
        if platform == "darwin": # macOS
            pync.notify(
                f"No new videos.",
                title='rss-youtube-downloader',
                contentImage=iconCheckmark,
                sound=""
                # open=
                )
        elif platform == "win32": # Windows
            toaster.show_toast(
                title="rss-youtube-downloader", 
                msg=
                f"No new videos.",
                icon_path="icons/checkmark.ico",
                duration=None,
                threaded=True
                # callback_on_click=
                ) # duration=None - leave notification in Notification Center; threaded=True - rest of the script will be allowed to be executed while the notification is still active
    else:
        while read_RSS.entries[counter].link not in file_content: # if video is new (not in the file of past downloads) then go and download; if not -> skip 

        # break if end of the list 
            if counter < 0: 
                break

            print(f"Video # (1 = newest): {counter+1}") # debug / status

            # channel URL
            # print(f"Channel URL: {read_RSS.feed.link}") # print channel URL 

            # video title
            videoTitle = read_RSS.entries[counter].title # get latest video's title
            print(f"Video's title: {videoTitle}") # print the latest video's URL

            # video URL
            videoURL = read_RSS.entries[counter].link # get the latest video's URL
            print(f"Video's URL: {videoURL}") # print the latest video's URL

            # download video
            downloadVideo(videoURL)

            counter = counter - 1 # go up the list to the [0] newest video 

except: # file doesn't exist and can't read it, no internet connection, wrong feed URL
    print("Issues with the checker. Closing...")

# ----------- fun ends here ---------- #

# ------------- run time ------------- #

end_time = time.time() # run time end 
total_run_time = round(end_time-start_time,2)
print(f"Total script run time: {total_run_time} seconds.")
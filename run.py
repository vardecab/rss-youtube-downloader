# ==================================== #
#        rss-youtube-downloader        #
# ==================================== #

# ------------ import libs ----------- #
#region

# core ↓
import yt_dlp # download YouTube videos # NOTE: https://github.com/ytdl-org/youtube-dl/issues/30102#issuecomment-943849906
import feedparser # read RSS

# other ↓
import time # calculate script's run time
# from datetime import datetime # generate timestamp for saving data
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
if platform == 'darwin': # check if user is using macOS
    import ssl
    if hasattr(ssl, '_create_unverified_context'):
        ssl._create_default_https_context = ssl._create_unverified_context

#endregion
# --------- start + run time --------- #
#region

startTime = time.time() # run time start
print("Starting the script...") # status

# ----- timestamp for saving data ---- #

# thisRunDatetime = timestamp = datetime.strftime(datetime.now(), '%y%m%d-%H%M%S') # eg. 210120-173112

# ----- check and create folders ----- #

# files
# if not os.path.isdir("###"): # if folder doesn't exist
#     os.mkdir("###") # create folder 
#     print("Folder created: ###") # status

#endregion
# ---------- fun begins here --------- #

# ---------- download video ---------- #

# TODO: exclude segments with SponsorBlock parameters
# TODO: convert to .mp3?

def downloadVideo(videoURL):
    
    downloadPath = r'/Users/x/TV Shows/' # download location

    #  parameters for the downloader
    optionalParameters = { 
        'quiet': True, # don't throw status messages in the console
        'outtmpl': downloadPath + r'/%(title)s.%(ext)s' # download location + name of the file
        } 

    try:
        with yt_dlp.YoutubeDL(optionalParameters) as YouTubeDownloader:
            # videoInfo = YouTubeDownloader.extract_info(videoURL, download=False) # get info (title, metadata, etc.) about the video without downloading
            
            print("Downloading the video...") # status
            YouTubeDownloader.download(videoURL) # now download the video
            # print("Video downloaded or it's already on the disk.") # status
            print("Video downloaded.") # status
            # TODO: how to check if downloading or already on disk?
            
            # notifications 
            if platform == "darwin": # macOS
                pync.notify(
                    # f"Video from {readRSS.feed.title} downloaded or already on the disk.",
                    f"Video from {readRSS.feed.title} downloaded.",
                    title='rss-youtube-downloader',
                    contentImage=iconDownload,
                    sound=""
                    # open= # TODO: URL
                    )
            elif platform == "win32": # Windows
                toaster.show_toast(
                    title="rss-youtube-downloader", 
                    msg=
                    # f"Video from {readRSS.feed.title} downloaded or already on the disk.",
                    f"Video from {readRSS.feed.title} downloaded.",
                    icon_path="icons/download.ico",
                    duration=None,
                    threaded=True
                    # callback_on_click= # TODO: check if works without it; function with URL
                    ) # duration=None - leave notification in Notification Center; threaded=True - rest of the script will be allowed to be executed while the notification is still active
            
            with open('videos.txt','a') as saveFile: # create a text file
                saveFile.write(videoURL + "\n") # save video URL to the file
                # NOTE: not very pretty but works # TODO: avoid duplicates 

    except: # Internet down, wrong URL
        print(f"Can't download the video. Check your internet connection and video's URL ({videoURL}), then try again. Closing...") # status

# ------------- read RSS ------------- #

# TODO: get input + default on timeout 
# TODO: ask which feed to check, type 1/2/3/4/5 or name of the channel 

def readingRSS(RSSfeed):
    try:
        readRSS = feedparser.parse(RSSfeed) # read the RSS feed
        print(f"Reading RSS feed: {readRSS.feed.title} ({RSSfeed})") # status
        return readRSS # get it outside of the function
    except: 
        print(f"Can't read the RSS feed. Maybe there is a problem with your internet connection or with the `RSSfeed` URL: {RSSfeed}. Closing...")
        exit()

# ------ map feeds to variables ------ #

RSSfeed1 = 'https://www.youtube.com/feeds/videos.xml?channel_id=UC8LJZNHnqXKg5TMgyvxszPA' # Budda
RSSfeed2 = 'https://www.youtube.com/feeds/videos.xml?channel_id=UCBJycsmduvYEL83R_U4JriQ' # MKBHD

# -------- add feeds to a list ------- #

RSSfeeds = [RSSfeed1, RSSfeed2] # create a list of feeds
print(f"How many feeds / channels we need to check: {len(RSSfeeds)}") # status

# -- read / create .txt file w/ URLs - #

try:
    with open('videos.txt', 'r') as openFile: # open file
        fileContent = openFile.read() # read file
except: 
    with open('videos.txt', 'w') as openFile: # create a file
        print("There was a problem with reading the `videos.txt` file. It didn't exist so it was created now.")
    with open('videos.txt', 'r') as openFile: # open file
        fileContent = openFile.read() # read file

# ------------ core stuff ------------ #
    
counterVideoLookback = 1 # NOTE: how far back we should look for the videos (3 = 4 videos back, 10 = 11 videos back, 0 = just newest video)
    # FIX: not working when eg. 2nd video downloaded and you're looking for the 1st and 3rd
    # NOTE: check line #202 too
counterFeedList = 0 # go through feeds in the list

try:
    while counterFeedList < len(RSSfeeds): # if counter smaller than number of feeds in the list
        readRSS = readingRSS(RSSfeeds[counterFeedList])
        if readRSS.entries[counterVideoLookback].link in fileContent:
            print(f"Newest video from {readRSS.feed.title} already watched or downloaded and available on the disk.")
            # notifications 
            if platform == "darwin": # macOS
                pync.notify(
                    f"No new videos from: {readRSS.feed.title}.",
                    title='rss-youtube-downloader',
                    contentImage=iconCheckmark,
                    sound=""
                    # open= # TODO: URL
                    )
            elif platform == "win32": # Windows
                toaster.show_toast(
                    title="rss-youtube-downloader", 
                    msg=
                    f"No new videos from: {readRSS.feed.title}.",
                    icon_path="icons/checkmark.ico",
                    duration=None,
                    threaded=True
                    # callback_on_click= # TODO: check if works without it; function with URL
                    ) # duration=None - leave notification in Notification Center; threaded=True - rest of the script will be allowed to be executed while the notification is still active
        else:
            while readRSS.entries[counterVideoLookback].link not in fileContent: # if video is new (not in the file of past downloads) then go and download; if not -> skip 

            # break if end of the list 
                if counterVideoLookback < 0: 
                    break

                print(f"Video # (1 = newest): {counterVideoLookback+1}") # debug / status

                # channel URL
                # print(f"Channel URL: {readRSS.feed.link}") # print channel URL 
                
                # channel name
                # print(f"Channel name: {readRSS.feed.title}") # print channel name 

                # video title
                videoTitle = readRSS.entries[counterVideoLookback].title # get latest video's title
                print(f"Video's title: {videoTitle}") # print the latest video's URL

                # video URL
                videoURL = readRSS.entries[counterVideoLookback].link # get the latest video's URL
                print(f"Video's URL: {videoURL}") # print the latest video's URL

                # download video
                downloadVideo(videoURL) # send URL to function

                counterVideoLookback = counterVideoLookback - 1 # go up the list to the [0] newest video
        counterFeedList = counterFeedList + 1
        counterVideoLookback = 1 # reset variable to original value from before the loops # TODO: shady

except: # file doesn't exist and can't read it, no internet connection, wrong feed URL
    print("Issues with the checker. Closing...") # TODO: write something more descriptive

# ----------- fun ends here ---------- #

# ------------- run time ------------- #
#region

endTime = time.time() # run time end 
totalRunTime = round(endTime-startTime,2)
print(f"Total script run time: {totalRunTime} seconds.")

#endregion
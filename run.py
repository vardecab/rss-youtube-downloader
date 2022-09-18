# ==================================== #
#        rss-youtube-downloader        #
# ==================================== #

# ------------ import libs ----------- #

# core ↓
import yt_dlp # download YouTube videos # NOTE: https://github.com/ytdl-org/youtube-dl/issues/30102#issuecomment-943849906
import feedparser # read RSS

# other ↓
import time # calculate script's run time

# notifications ↓ 
from sys import platform # check platform (Windows/macOS)
if platform == 'darwin':
    import pync # macOS notifications
elif platform == 'win32':
    from win10toast_click import ToastNotifier # Windows 10/11 notifications
    toaster = ToastNotifier() # initialize win10toast
    
iconDownload = "icons/download.png" # location of icon
iconCheckmark = "icons/checkmark.png" # location of icon

# solution ↓
# NOTE: fix certificate issue -> https://stackoverflow.com/questions/28282797/feedparser-parse-ssl-certificate-verify-failed
if platform == 'darwin': # check if user is using macOS
    import ssl
    if hasattr(ssl, '_create_unverified_context'):
        ssl._create_default_https_context = ssl._create_unverified_context

# --------- start + run time --------- #

startTime = time.time() # run time start
print("Starting the script...") # status

# ---------- fun begins here --------- #

# ---------- download video ---------- #

# TODO: exclude segments with SponsorBlock parameters? might not work if download is triggered right after video is published
# TODO: convert to .mp3? useful for music

def downloadVideo(videoURL):
    
    downloadPath = r'/Users/x/TV Shows/YouTube Downloads' # download location

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
            print("Video downloaded.") # status
            # TODO: how to check if downloading or already on disk?
            
            # notifications 
            if platform == "darwin": # macOS
                pync.notify(
                    f"Video from {readRSS.feed.title} downloaded.",
                    title='rss-youtube-downloader',
                    contentImage=iconDownload,
                    sound=""
                    # open=videoURL
                    )
            elif platform == "win32": # Windows
                toaster.show_toast(
                    title="rss-youtube-downloader", 
                    msg=f"Video from {readRSS.feed.title} downloaded.",
                    icon_path="icons/download.ico",
                    duration=None,
                    threaded=True
                    # callback_on_click= 
                    ) # duration=None - leave notification in Notification Center; threaded=True - rest of the script will be allowed to be executed while the notification is still active
            
            # save video URL to a file for checks in future
            with open('videos.txt','a') as saveFile: # create a text file
                # duplicates are avoided because only new videos (not present in the file) rare saved
                saveFile.write(videoURL + "\n") # save video URL to the file
    except: # Internet down, wrong URL
        print(f"Can't download the video. Check your internet connection and video's URL ({videoURL}), then try again. Closing...") # status

# ------------- read RSS ------------- #

def readingRSS(RSSfeed):
    try:
        readRSS = feedparser.parse(RSSfeed) # read the RSS feed
        print(f"Reading RSS feed: {readRSS.feed.title} ({RSSfeed})") # status
        return readRSS # get it outside of the function
    except: 
        print(f"Can't read the RSS feed. Maybe there is a problem with your internet connection or with the `RSSfeed` URL: {RSSfeed}. Closing...") # status
        exit() # end the script

# -------- add feeds to a list ------- #

# create a list of feeds
RSSfeeds = [
    'https://www.youtube.com/feeds/videos.xml?channel_id=UC8LJZNHnqXKg5TMgyvxszPA', # Budda
    'https://www.youtube.com/feeds/videos.xml?channel_id=UCBJycsmduvYEL83R_U4JriQ' # MKBHD
    ] 

print(f"How many feeds / channels we need to check: {len(RSSfeeds)}") # status

# -- read / create .txt file w/ URLs - #

try: # try to open file
    with open('videos.txt', 'r') as openFile: # open file
        fileContent = openFile.read() # read file
except: # if it doesn't exist, create it
    with open('videos.txt', 'w') as openFile: # create a file
        print("There was a problem with reading the `videos.txt` file. It didn't exist so it was created now.") # status
    with open('videos.txt', 'r') as openFile: # open file
        fileContent = openFile.read() # read file

# ------------ core stuff ------------ #

counterFeedList = 0 # go through feeds in the list

try:
    while counterFeedList < len(RSSfeeds): # if counter smaller than number of feeds in the list; iterate through the feed list
        counterVideoLookback = 0 # NOTE: how far back we should look for the videos (3 = 4 videos back, 10 = 11 videos back, 0 = just newest video)
        # FIX: not working when eg. 2nd video downloaded and you're looking for the 1st and 3rd
        readRSS = readingRSS(RSSfeeds[counterFeedList]) #  throw feed to the function and get the data back so we can use it
        if readRSS.entries[0].link in fileContent: # check if the newest video is watched / downloaded
            print(f"Newest video from {readRSS.feed.title} already watched or downloaded and available on the disk.")
            # notifications 
            if platform == "darwin": # macOS
                pync.notify(
                    f"No new videos from: {readRSS.feed.title}.",
                    title='rss-youtube-downloader',
                    contentImage=iconCheckmark,
                    sound=""
                    # open= 
                    )
            elif platform == "win32": # Windows
                toaster.show_toast(
                    title="rss-youtube-downloader", 
                    msg=f"No new videos from: {readRSS.feed.title}.",
                    icon_path="icons/checkmark.ico",
                    duration=None,
                    threaded=True
                    # callback_on_click=
                    ) # duration=None - leave notification in Notification Center; threaded=True - rest of the script will be allowed to be executed while the notification is still active
        else:
            while readRSS.entries[counterVideoLookback].link not in fileContent: # if video is new (not in the file of past downloads) then go and download; if not -> skip 
                
            # break if we have enough videos 
                if counterVideoLookback >= 2: # NOTE: how far we should look (2 = 3 videos); stop so we don't download too many videos 
                    print(f"That should be enough. Moving on...") # status 
                    break

                print(f"Downloading video # (1 = newest): {counterVideoLookback+1}") # status

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

                counterVideoLookback = counterVideoLookback + 1 # go up the list to the older video
            else:
                counterVideoLookback = counterVideoLookback + 1 # go up the list to the older video
        counterFeedList = counterFeedList + 1 # continue with the next feed in the list   
except: # file doesn't exist and can't read it, no internet connection, wrong feed URL
    print("Issues with the checker. Closing...") # TODO: write something more descriptive and helpful

# ----------- fun ends here ---------- #

# ------------- run time ------------- #

endTime = time.time() # run time end 
totalRunTime = round(endTime-startTime,2)
print(f"Total script run time: {totalRunTime} seconds. That's {round(totalRunTime/60,2)} minutes.")
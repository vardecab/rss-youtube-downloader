# ==================================== #
#        rss-youtube-downloader        #
# ==================================== #

# ------------ import libs ----------- #

# core ↓
import yt_dlp  # download YouTube videos # NOTE: https://github.com/ytdl-org/youtube-dl/issues/30102#issuecomment-943849906
import feedparser  # read RSS

# other ↓
import time  # calculate script's run time
import os  # create download path

# notifications ↓
from sys import platform  # check platform (Windows/macOS)
if platform == 'darwin':
    import pync  # macOS notifications
    # icons
    iconDownload = "icons/download.png" 
    iconCheckmark = "icons/checkmark.png"  
elif platform == 'win32':
    from plyer import notification  # Windows notification

# solution ↓
# NOTE: certificate issue -> https://stackoverflow.com/questions/28282797/feedparser-parse-ssl-certificate-verify-failed
if platform == 'darwin':  # check if user is using macOS
    import ssl
    if hasattr(ssl, '_create_unverified_context'):
        ssl._create_default_https_context = ssl._create_unverified_context

# --------- start + run time --------- #

startTime = time.time()  # run time start
print("Starting the script...")  # status

# ---------- fun begins here --------- #

# ---------- download video ---------- #


def downloadMusic(videoURL):

    # ------ create download folder ------ #

    downloadFolderName = 'Podcasts'

    if platform == 'darwin':
        # download location on macOS
        downloadParentFolder = r'/Users/q/Library/Mobile Documents/com~apple~CloudDocs/iCloud/'
        # downloadParentFolder = r'/Users/q/Downloads'
        # downloadParentFolder = r'/Users/q/Movies/YouTube Downloads/TEMP'
    elif platform == 'win32':
        # download location on Windows
        downloadParentFolder = r'C:/Users/x/Videos/'

    # check if the folder exists in the parent folder
    downloadPath = os.path.join(downloadParentFolder, downloadFolderName)
    # if os.path.exists(downloadPath):
    #     pass
    # else:
    #     # create the folder
    #     os.makedirs(downloadPath)
    #     print(
    #         f'Folder "{downloadFolderName}" was created. Go here: "{downloadPath}".')

    # create path from download location ^ + channel name (use if exists, create if it doesn't)
    # downloadPath = os.path.join(downloadPath, channelName)

    #  parameters for the downloader
    optionalParameters = {
        # INFO: video
        # # format: max 1080p; .mp4 instead of default .webm # NOTE: ChatGPT
        # 'format': 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/mp4',

        # # download with better speed # NOTE: ChatGPT
        # 'external_downloader': 'aria2c',
        # # param definitions ↓
        # 'external_downloader_args': ['-x', '16', '-s', '16', '-k', '100M'],
        # # `-s 16`: This option specifies the number of segments to split the download into. A higher number can improve download speed, but may cause the server to block the download. In this case, it is set to 16 segments.
        # # `-k 100M`: This option sets the maximum size of each segment to 100 megabytes (MB). This can also help improve download speed, as the downloader will download smaller chunks of the file at a time.

        # 'quiet': True,  # don't throw status messages in the console

        # # download location + name of the file
        # 'outtmpl': downloadPath + r'/%(title)s.%(ext)s',

        # # SponsorBlock
        # 'sponsorblock_remove': True, # use SponsorBlock 
        # 'postprocessors': [{
        #     'key': 'SponsorBlock',
        #     'categories': ['sponsor', 'selfpromo', 'interaction'] # segments that have to be removed
        # }, {
        #     'key': 'ModifyChapters',
        #     'remove_sponsor_segments': ['sponsor', 'selfpromo', 'interaction'] # segments that have to be removed
        # }]
        
        # INFO: music
        'quiet': True, # don't throw status messages in the console
        'format': 'bestaudio/best', # download with best audio
        'outtmpl': downloadPath + r'/%(title)s.%(ext)s', # download location + name of the file
        'postprocessors': [{
            # extract music from video
            'key': 'FFmpegExtractAudio', # extract audio from the video file
            'preferredcodec': 'mp3', # codec
            'preferredquality': '320', # 320 kbps quality 
        }],


    }

    try:
        with yt_dlp.YoutubeDL(optionalParameters) as YouTubeDownloader:
            # videoInfo = YouTubeDownloader.extract_info(videoURL, download=False) # get info (title, metadata, etc.) about the video without downloading

            print("Downloading the video...")  # status
            YouTubeDownloader.download(videoURL)  # now download the video
            print("Video downloaded.")  # status
            # TODO: how to check if downloading or already on disk?

            # notifications
            if platform == "darwin":  # macOS
                pync.notify(
                    f"Video from {readRSS.feed.title} downloaded.",
                    title='rss-youtube-downloader',
                    contentImage=iconDownload,
                    sound=""
                    # open=videoURL
                )
            elif platform == "win32":  # Windows
                notification.notify(
                    title='rss-youtube-downloader',
                    message=f"Video from {readRSS.feed.title} downloaded.",
                    app_icon='icons/download.ico')

                # save video URL to a file for checks in future
            with open('videos.txt', 'a') as saveFile:  # create a text file
                # duplicates are avoided because only new videos (not present in the file) rare saved
                saveFile.write(videoURL + "\n")  # save video URL to the file
    except:  # Internet down, wrong URL
        # status
        print(
            f"Can't download the video. Check your internet connection and video's URL ({videoURL}), then try again. Closing...")

# ------------- read RSS ------------- #


def readingRSS(RSSfeed):
    try:
        readRSS = feedparser.parse(RSSfeed)  # read the RSS feed
        print(f"Reading RSS feed: {readRSS.feed.title} ({RSSfeed})")  # status
        return readRSS  # get it outside of the function
    except:
        # status
        print(
            f"Can't read the RSS feed. Maybe there is a problem with your internet connection or with the `RSSfeed` URL: {RSSfeed}. Closing...")
        exit()  # end the script

# -------- add feeds to a list ------- #

# get channel RSS
# 1. Go to source page of the channel.
# 2. Look for "com/channel".
# 3. Copy ID, eg. "UC6n8I1UDTKP1IWjQMg6_TwA"
# 4. Add it to: "https://www.youtube.com/feeds/videos.xml?channel_id=CHANNELID"
# 5. https://www.youtube.com/feeds/videos.xml?channel_id=UC6n8I1UDTKP1IWjQMg6_TwA


# create a list of feeds
RSSfeeds = [
    'https://www.youtube.com/feeds/videos.xml?channel_id=UC8JbbaZ_jgdsoUqrZ2bXtQQ' # Lekko Stronniczy
    # 'https://www.youtube.com/feeds/videos.xml?channel_id=UC8LJZNHnqXKg5TMgyvxszPA',  # Budda
    # 'https://www.youtube.com/feeds/videos.xml?channel_id=UCBJycsmduvYEL83R_U4JriQ',  # MKBHD
    # 'https://www.youtube.com/feeds/videos.xml?channel_id=UC6n8I1UDTKP1IWjQMg6_TwA'  # B1M
    # 'https://www.youtube.com/feeds/videos.xml?playlist_id=PLESJyWkLUYUhhZleYHyWf177bduR2Thln',  # Basket Office
    # 'https://www.youtube.com/feeds/videos.xml?playlist_id=PLlVlyGVtvuVkM5S4-_IzLDpInhd04W5GJ', # NBA Top Plays of the Week
    # 'https://www.youtube.com/feeds/videos.xml?playlist_id=PLlVlyGVtvuVl8kzNkZoPhKIkMXmNvtGZV', # NBA Uncut
    # 'https://www.youtube.com/feeds/videos.xml?playlist_id=PLlVlyGVtvuVlJUCo0M8Nzj-dsGBexP6Bk', # NBA Fantastic Finishes
    # 'https://www.youtube.com/feeds/videos.xml?playlist_id=PLlVlyGVtvuVlZh5EYXYBl1ao6QnvVEice', # NBA Top Plays Of The Night
    # 'https://www.youtube.com/feeds/videos.xml?playlist_id=PLlVlyGVtvuVkpQeaF_AvbkZN9F9dXW0aC', # NBA Top Performances
    # 'https://www.youtube.com/feeds/videos.xml?playlist_id=PLU6BYY1Lu_feVbuZEscpd6xT32zCrVrev' # NBA Shaqtin' A Fool
    
]

# if no feeds then terminate the script
if len(RSSfeeds) <= 0:
    print("No RSS feeds in the list, let's end the party.")
    exit()

print(f"How many feeds / channels we need to check: {len(RSSfeeds)}")  # status

# -- read / create .txt file w/ URLs - #

try:  # try to open file
    with open('videos.txt', 'r') as openFile:  # open file
        fileContent = openFile.read()  # read file
except:  # if it doesn't exist, create it
    with open('videos.txt', 'w') as openFile:  # create a file
        # status
        print("There was a problem with reading the `videos.txt` file. It didn't exist so it was created now.")
    with open('videos.txt', 'r') as openFile:  # open file
        fileContent = openFile.read()  # read file

# ------------ core stuff ------------ #

counterFeedList = 0  # go through feeds in the list

# try:
# if counter smaller than number of feeds in the list; iterate through the feed list
while counterFeedList < len(RSSfeeds):
    # how far back we should look for the videos (3 = 4 videos back, 10 = 11 videos back, 0 = just newest video)
    counterVideoLookback = 0
    # TODO: not working when eg. 2nd video downloaded and you're looking for the 1st and 3rd
    # throw feed to the function and get the data back so we can use it
    readRSS = readingRSS(RSSfeeds[counterFeedList])
    # check if the newest video is watched / downloaded
    if readRSS.entries[0].link in fileContent:
        print(
            f"Newest video from {readRSS.feed.title} already watched or downloaded and available on the disk.")
        # notifications
        if platform == "darwin":  # macOS
            # pync.notify(
            #     f"No new videos from: {readRSS.feed.title}.",
            #     title='rss-youtube-downloader',
            #     contentImage=iconCheckmark,
            #     sound=""
            print
                # open=
            # )
        elif platform == "win32":  # Windows
            notification.notify(
                title='rss-youtube-downloader',
                message=f"No new videos from: {readRSS.feed.title}.",
                app_icon='icons/checkmark.ico')
    else:
        # if video is new (not in the file of past downloads) then go and download; if not -> skip
        while readRSS.entries[counterVideoLookback].link not in fileContent:

            # break if we have enough videos
            # how far we should look (2 = 3 videos); stop so we don't download too many videos
            if counterVideoLookback >= 5:
                print(f"That should be enough. Moving on...")  # status
                break
            # FIX: doesn't work if you want to download more but newest is already downloaded 

            # status
            print(
                f"Downloading video # (1 = newest): {counterVideoLookback+1}")

            # channel URL
            # print(f"Channel URL: {readRSS.feed.link}") # print channel URL

            # channel name
            # print(f"Channel name: {readRSS.feed.title}") # print channel name

            # video title
            # get latest video's title
            videoTitle = readRSS.entries[counterVideoLookback].title
            # print the latest video's URL
            print(f"Video's title: {videoTitle}")

            # video URL
            # get the latest video's URL
            videoURL = readRSS.entries[counterVideoLookback].link
            # print the latest video's URL
            print(f"Video's URL: {videoURL}")

            # download video
            # downloadMusic(videoURL, readRSS.feed.title)  # send URL to function
            downloadMusic(videoURL)  # send URL to function

            counterVideoLookback = counterVideoLookback + \
                1  # go up the list to the older video
        else:
            counterVideoLookback = counterVideoLookback + \
                1  # go up the list to the older video
    counterFeedList = counterFeedList + 1  # continue with the next feed in the list
# except:  # file doesn't exist and can't read it, no internet connection, wrong feed URL
# TODO: write something more descriptive and helpful
    # print("Issues with the checker. Closing...")

# ----------- fun ends here ---------- #

# ------- move NBA files around ------ #

# import shutil  # for moving files
# import os  # for directory operations

# # List of source folders
# source_folders = [
#     '/Users/q/Movies/YouTube Downloads/Top Performances | 2024-25',
#     '/Users/q/Movies/YouTube Downloads/NBA Top Plays Of The Night | 2024-25',
#     '/Users/q/Movies/YouTube Downloads/Fantastic Finishes | 2024-25',
#     '/Users/q/Movies/YouTube Downloads/Uncut | 2024-25',
#     '/Users/q/Movies/YouTube Downloads/Top Plays of the Week | 2024-25',
#     r"/Users/q/Movies/YouTube Downloads/Shaqtin' A Fool"  # Use raw string to avoid escape issues
# ]

# Destination folder
# destination_folder = '/Users/q/Movies/YouTube Downloads/NBA'

# # Move files from all source folders to the destination folder
# for source_folder in source_folders:
#     if os.path.exists(source_folder):  # Check if the source folder exists
#         for filename in os.listdir(source_folder):
#             file_path = os.path.join(source_folder, filename)
#             if os.path.isfile(file_path):  # Check if it's a file
#                 destination_path = os.path.join(destination_folder, filename)
                
#                 # Check if the destination file already exists
#                 if os.path.exists(destination_path):
#                     # Create a new filename by appending a number to avoid conflict
#                     base, extension = os.path.splitext(filename)
#                     counter = 1
#                     new_filename = f"{base} ({counter}){extension}"
#                     new_destination_path = os.path.join(destination_folder, new_filename)
                    
#                     # Increment the counter until a unique filename is found
#                     while os.path.exists(new_destination_path):
#                         counter += 1
#                         new_filename = f"{base} ({counter}){extension}"
#                         new_destination_path = os.path.join(destination_folder, new_filename)
                    
#                     # Move the file to the new destination path
#                     shutil.move(file_path, new_destination_path)  # move file
#                 else:
#                     # Move the file if it doesn't exist in the destination
#                     shutil.move(file_path, destination_path)  # move file
#     else:
#         print(f"Source folder '{source_folder}' does not exist. Skipping...")  # Notify if folder doesn't exist

# Remove source folders regardless of file presence in destination
# for source_folder in source_folders:
#     if os.path.exists(source_folder):  # Check if the source folder exists before removing
#         shutil.rmtree(source_folder)  # remove the folder and its contents

# print(f"All files moved to '{destination_folder}' and source folders removed.")

# ------------- run time ------------- #

endTime = time.time()  # run time end
totalRunTime = round(endTime-startTime, 2)
print(
    f"Total script run time: {totalRunTime} seconds. That's {round(totalRunTime/60,2)} minutes.")

# rss-youtube-downloader

![Actively Maintained](https://img.shields.io/badge/Maintenance%20Level-Actively%20Maintained-green.svg)
<br>
![](https://img.shields.io/badge/platform-Windows%20%7C%20macOS-blue)

>Experimenting a bit with RSS + auto-downloading videos from YouTube.

<!-- ## Screenshots -->

<!-- ### Windows -->

<!-- ![1]() -->

<!-- ### macOS -->
<!-- ![1]() -->
<!-- ![2]() -->

<!-- ## How to use

1. Take your favourite YouTube channel URL: https://www.youtube.com/channel/UC8JbbaZ_jgdsoUqrZ2bXtQQ
2. Get channel ID either from the URL or by going here: https://commentpicker.com/youtube-channel-id.php
3. Use channel ID in the code. -->

## Release History

- 0.8: New library used for displaying Windows notifications; create download folder if it doesn't exist; dowloading files in `.mp4` instead of default `.webm` for improved compatibility; using external downloader to improve download speeds; added SponsorBlock to remove promo segments from videos.
- 0.7: Added code to create a download folder if it doesn't exist; added different download path for Windows.
- 0.6.1: Removed unnecessary code; added comments.
- 0.6: Rewrote some core logic to better handle new files.
- 0.5: Checking multiple feeds at once; changed variables from snake_case to camelCase; improved messages.
- 0.4.1: Tiny fix to platform check.
- 0.4: Added notifications.
- 0.3: Fixed the script on macOS; added checker to avoid duplicates; re-wrote the script to handle multiple videos.
- 0.2: Added RSS reader so now the script downloads the latest video from the RSS feed.
- 0.1: Initial release.

<!-- <details> -->

<!-- <summary>
Click to see all updates < 1.0.0
</summary> -->

<!-- - 0.2: 
- 0.1: Initial release.
</details> -->

<!-- <br> -->

## Versioning

Using [SemVer](http://semver.org/).

## License

![](https://img.shields.io/github/license/vardecab/youtube-downloader)

## Acknowledgements

- [feedparser](https://pypi.org/project/feedparser/) to read RSS feeds
- [yt-dlp](https://pypi.org/project/yt-dlp/) to download videos
- [ChatGPT](https://chat.openai.com/chat)
- Icons from [Flaticon](https://www.flaticon.com)
- PNG → ICO conversion with [ConvertICO](https://convertico.com)
- Windows notifications done with: [plyer](https://pypi.org/project/plyer/)
- macOS notifications done with: [pync](https://github.com/SeTeM/pync)

## Contributing

![](https://img.shields.io/github/issues/vardecab/youtube-downloader)

If you found a bug or want to propose a feature, feel free to visit [the Issues page](https://github.com/vardecab/youtube-downloader/issues).


from src.YTdownloader import YTDownloader
import sys

def downloader(link) -> None:

    yt_downloader = YTDownloader(rate_limit=9000000, format='mp4')

    # Download all videos of a channel
    if url.startswith(('https://www.youtube.com/c/', 'https://www.youtube.com/channel/', 'https://www.youtube.com/user/')):
        yt_downloader.download_channel_allvideo(link)

    # Download all videos in a playlist
    elif url.startswith('https://www.youtube.com/playlist'):
        yt_downloader.download_playlist(link)

    # Download single video from url
    elif url.startswith(('https://www.youtube.com/watch', 'https://www.twitch.tv/', 'https://clips.twitch.tv/')):
        yt_downloader.download_video(link)

    else:
        print("Invalid URL")


try:
    url = sys.argv[1]
    downloader(url)

except Exception as ex:
    sys.exit('Usage: python ytdl_run.py "URL" ')


# python ytdl_run.py "https://www.youtube.com/watch?v=j5-yKhDd64s&ab_channel=EminemVEVO"

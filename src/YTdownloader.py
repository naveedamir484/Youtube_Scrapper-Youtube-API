import yt_dlp

PATH = r"./Youtube_downloads"


class YTDownloader:

    def __init__(self, rate_limit=9000000, format='mp4') -> None:
        self.rate_limit = rate_limit
        self.format = f'best[ext={format}]'

    def download_video(self, video_link) -> None:

        yt_output = dict(
            ignoreerrors=True,
            abort_on_unavailable_fragments=True,
            format=self.format,
            outtmpl=PATH+'\\Videos\%(title)s ## %(uploader)s ## %(id)s.%(ext)s',
            ratelimit=self.rate_limit)

        if yt_output is not None:
            with yt_dlp.YoutubeDL(yt_output) as ydl:
                ydl.download(video_link)

    def download_playlist(self, playlist_link) -> None:

        yt_output = dict(
            ignoreerrors=True,
            abort_on_unavailable_fragments=True,
            format=self.format,
            outtmpl=PATH+'\\Playlists\%(playlist_uploader)s ## %(playlist)s\%(title)s ## %(uploader)s ## %(id)s.%(ext)s',
            ratelimit=self.rate_limit)

        if yt_output is not None:
            with yt_dlp.YoutubeDL(yt_output) as ydl:
                ydl.download(playlist_link)

    def download_channel_allvideo(self, channel_link) -> None:

        yt_output = dict(
            ignoreerrors=True,
            abort_on_unavailable_fragments=True,
            format=self.format,
            outtmpl=PATH + '\\Channels\%(uploader)s\%(title)s ## %(uploader)s ## %(id)s.%(ext)s',
            ratelimit=self.rate_limit)

        if yt_output is not None:
            with yt_dlp.YoutubeDL(yt_output) as ydl:
                ydl.download(channel_link)

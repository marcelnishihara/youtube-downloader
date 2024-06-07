"""Main Module
"""

from classes.youtube_dowloader import YouTubeDownloader


if __name__ == '__main__':
    videos = YouTubeDownloader.get_videos_urls_from_channel(
        channel_username='ensinobasic'
    )

    YouTubeDownloader.download(list_of_videos=videos)

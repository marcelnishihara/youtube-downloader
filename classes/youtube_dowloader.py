import json

from datetime import datetime
from pytube import YouTube
from scrapetube import get_channel


class YouTubeDownloader:
    def __init__(self) -> None:
        pass


    @staticmethod
    def formatted_datetime() -> None:
        return (
            datetime
            .now()
            .strftime(format='%Y_%m_%d_%H_%M_%S_%Z')
        )


    @staticmethod
    def log(string: str = None) -> None:
        """_summary_

        Args:
            string (str, optional):
                _description_
        """
        now = YouTubeDownloader.formatted_datetime()
        filename = f'log_videos_data_{now}.json'

        with open(file=filename, mode='w', encoding='utf-8') as f:
            f.write(string)


    @classmethod
    def get_videos_urls_from_channel(
        cls,
        channel_id: str = None,
        channel_url: str = None,
        channel_username: str = None
    ) -> list:
        """_summary_

        Args:
            channel_id (str, optional):
                _description_.
            
            channel_url (str, optional):
                _description_.
            
            channel_username (str, optional):
                _description_.

        Raises:
            ValueError:
                _description_

        Returns:
            list:
                _description_
        """
        if channel_id:
            channel_videos = get_channel(channel_id=channel_id)
        elif channel_url:
            channel_videos = get_channel(channel_url=channel_url)
        elif channel_username:
            channel_videos = get_channel(channel_username=channel_username)
        else:
            raise ValueError('Missing parameter')

        return list(
            map(
                lambda video: {
                    'url': (
                        f'https://www.youtube.com/watch?v={video["videoId"]}'
                    )
                },
                list(channel_videos)
            )
        )


    @classmethod
    def download(
        cls,
        video: str = None,
        list_of_videos: list = None,
        output_path: str = './downloads/',
        get_video_data: bool = True
    ) -> None:
        """_summary_

        Args:
            video (str, optional): 
                _description_.
            list_of_videos (list, optional):
                _description_.
            output_path (str, optional):
                _description_.
                Defaults to ``'./downloads/'``
            get_video_data (bool, optional):
                _description_.
                Defaults to True.

        Raises:
            ValueError: 
                _description_
        """
        if video:
            list_of_videos += [{ 'url': video }]
        elif list_of_videos:
            for video in list_of_videos:
                youtube_video = YouTube(url=video['url'])
                publish_date = youtube_video.publish_date.strftime('%Y_%m_%d')

                video['publish_date'] = publish_date
                video['author'] = youtube_video.author
                video['title'] = youtube_video.title
                video['description'] = youtube_video.description
                video['thumbnail'] = youtube_video.thumbnail_url
                video['length'] = youtube_video.length
                video['channel_id'] = youtube_video.channel_id
                video['channel_url'] = youtube_video.channel_url
                video['views'] = youtube_video.views
                video['keywords'] = youtube_video.keywords

                try:
                    mp4_files = youtube_video.streams.filter(
                        file_extension='mp4',
                        progressive=True
                    )

                    higher_resolution = (
                        mp4_files
                        .order_by(attribute_name='resolution')
                        .desc()
                        .first()
                    )

                    filename = (
                        f'{publish_date}_{higher_resolution.title}'
                        .replace(' ', '_')
                        .replace('ª', 'a')
                        .replace('º', 'o')
                        .replace('.', '')
                    )

                    higher_resolution.download(
                        output_path=output_path,
                        filename=f'{filename}.mp4'
                    )

                    video['download_success'] = True

                except Exception as download_err:
                    print(
                        'An error occoured while the tried to '
                        f'download the video {video["url"]}: '
                        f'{download_err}'
                    )

                    video['download_success'] = False

            if get_video_data:
                YouTubeDownloader.log(
                    string=json.dumps(
                        obj=list_of_videos,
                        indent=4
                    )
                )

        else:
            raise ValueError('Missing parameter')

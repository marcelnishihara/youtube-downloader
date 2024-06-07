"""Main Module
"""

import json

from pytube import YouTube


if __name__ == '__main__':
    videos = [
        {
            'url' : ''
        }
    ]

    for video in videos:
        try:
            youtube_video = YouTube(url=video['url'])
            video_streams = youtube_video.streams
            mp4_files = video_streams.filter(file_extension='mp4')
            mp4_files = mp4_files.order_by(attribute_name='resolution').desc()
            higher_resolution = mp4_files.first()

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

            filename = (
                f'{publish_date}_{higher_resolution.title.replace(' ', '_')}'
            )

            video_streams.get_audio_only().download(
                output_path='./downloads/',
                filename=f'{filename}_audio.mp4'
            )

            higher_resolution.download(
                output_path='./downloads/',
                filename=f'{filename}_video.mp4'
            )

        except Exception as err:
            print(err)


    with open(file='videos_data.json', mode='w', encoding='utf-8') as f:
        f.write(json.dumps(obj=videos, indent=4))

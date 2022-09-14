from googleapiclient.discovery import build
from src.keys import API_KEY

class Scrapper:

    def __init__(self) -> None:

        self.youtube = build('youtube', 'v3', developerKey=API_KEY)

    def get_channel_detail(self, channel_id) -> list:

        all_data = []

        try:
            request = self.youtube.channels().list(
                part='snippet, contentDetails, statistics',
                id=channel_id)

            response = request.execute()

        except Exception as ex:
            print("Error in making request in get_channel_detail", ex)
            return None

        for i in range(len(response['items'])):

            try:

                all_playlists_detail = self.get_channel_playlists(channel_id=response['items'][i].get('id'))
                all_videos_detail = self.get_videos_detail(self.get_video_ids(response['items'][i]['contentDetails']['relatedPlaylists']['uploads']))

                data = dict(channel_name=response['items'][i]['snippet'].get('title'),
                            channel_id=response['items'][i].get('id'),
                            playlist_group_id=response['items'][i]['contentDetails']['relatedPlaylists'].get('uploads'),
                            subscriber_count=response['items'][i]['statistics'].get('subscriberCount'),
                            total_views=response['items'][i]['statistics'].get('viewCount'),
                            total_videos=response['items'][i]['statistics'].get('videoCount'),
                            logo_url=response['items'][i]['snippet']['thumbnails'].get('medium').get('url'),
                            published_date=response['items'][i]['snippet'].get('publishedAt'),
                            channel_desc=response['items'][i]['snippet'].get('description'),
                            all_playlists=all_playlists_detail,
                            all_videos=all_videos_detail)

                all_data.append(data)

            except Exception as ex:
                print(ex)


        return all_data


    def get_video_ids(self, playlist_id) -> list:

        video_ids = []
        next_page_token = None

        while True:

            try:
                request = self.youtube.playlistItems().list(
                    part='contentDetails',
                    playlistId=playlist_id,
                    maxResults=50,
                    pageToken=next_page_token)

                response = request.execute()

            except Exception as ex:
                print("Error in making request in get_video_ids", ex)
                return None

            for i in range(len(response['items'])):
                if response['items'][i]['contentDetails'].get('videoId') is not None:
                    video_ids.append(response['items'][i]['contentDetails']['videoId'])

            next_page_token = response.get('nextPageToken')

            if next_page_token is None:
                break

        return video_ids


    def get_videos_detail(self, video_ids) -> list:

        all_video_stats = []

        for i in range(0, len(video_ids), 50):

            try:
                request = self.youtube.videos().list(
                            part='snippet,statistics,id',
                            id=','.join(video_ids[i:i+50]))
                response = request.execute()

            except Exception as ex:
                print("Error in making request in get_videos_detail", ex)
                return None


            for video in response['items']:

                try:
                    video_stats = dict(
                         title=video['snippet']['title'],
                         video_link="https://www.youtube.com/watch?v="+str(video['id']),
                         channel_id=video['snippet']['channelId'],
                         view_count=video['statistics'].get('viewCount'),
                         like_count=video['statistics'].get('likeCount'),
                         comment_count=video['statistics'].get('commentCount'),
                         published_date=video['snippet']['publishedAt'],
                         video_thumbnail_url=video['snippet']['thumbnails']['medium']['url'],
                         video_desc=video['snippet']['description'])

                    all_video_stats.append({video['id']: video_stats})

                except Exception as ex:
                    print(ex)


        return all_video_stats

    def get_playlists_detail(self, playlist_ids) -> list:

        all_playlists_stats = []

        for k in range(0, len(playlist_ids), 50):

            try:

                request = self.youtube.playlists().list(
                    part='id,snippet, contentDetails',
                    id=','.join(playlist_ids[k:k+50]))

                response = request.execute()

            except Exception as ex:
                print("Error in making request in get_playlists_detail", ex)
                return None

            for i in range(len(response['items'])):

                try:

                    playlist_videos = self.get_videos_detail(self.get_video_ids(response['items'][i]['id']))

                    playlist = dict(
                        playlist_title=response['items'][i]['snippet']['title'],
                        item_count=response['items'][i]['contentDetails']['itemCount'],
                        playlist_thumbnail_url=response['items'][i]['snippet']['thumbnails']['medium']['url'],
                        playlist_desc=response['items'][i]['snippet']['description'],
                        playlist_vidoes=playlist_videos)

                    all_playlists_stats.append({response['items'][i]['id']: playlist})


                except Exception as ex:
                    print(ex)


        return all_playlists_stats


    def get_channel_playlists(self, channel_id) -> list:

        all_playlists = []
        next_page_token = None

        while True:

            try:

                request = self.youtube.playlists().list(
                    part='id,snippet, contentDetails',
                    channelId=channel_id,
                    maxResults=50,
                    pageToken=next_page_token)

                response = request.execute()

            except Exception as ex:
                print("Error in making request in get_channel_playlists", ex)
                return

            for i in range(len(response['items'])):

                try:

                    playlist_videos = self.get_videos_detail(self.get_video_ids(response['items'][i]['id']))

                    playlist = dict(
                        playlist_title=response['items'][i]['snippet']['title'],
                        playlist_id=response['items'][i]['id'],
                        item_count=response['items'][i]['contentDetails']['itemCount'],
                        playlist_thumbnail_url=response['items'][i]['snippet']['thumbnails']['medium']['url'],
                        playlist_desc=response['items'][i]['snippet']['description'],
                        playlist_vidoes=playlist_videos)

                    all_playlists.append(playlist)

                except Exception as ex:
                    print(ex)

            next_page_token = response.get('nextPageToken')

            if next_page_token is None:
                break

        return all_playlists



    def search_video_ids(self, keyword) -> list:

        video_ids = []
        next_page_token = None

        while True:

            try:

                request = self.youtube.search().list(
                    part="snippet",
                    q=keyword,
                    maxResults=50,
                    pageToken=next_page_token,
                    type="video")

                response = request.execute()

            except Exception as ex:
                print("Error in making request in search_videos", ex)
                return None


            for i in range(len(response['items'])):
                if response['items'][i]['id'].get('videoId') is not None:
                    video_ids.append(response['items'][i]['id'].get('videoId'))

            next_page_token = response.get('nextPageToken')

            if next_page_token is None:
                break

        return video_ids


    def search_channel_ids(self, keyword) -> list:

        channel_ids = []
        next_page_token = None

        while True:

            try:
                request = self.youtube.search().list(
                    part="snippet",
                    q=keyword,
                    maxResults=50,
                    pageToken=next_page_token,
                    type="channel")

                response = request.execute()

            except Exception as ex:
                print("error in making request in search_channels", ex)
                return None


            for i in range(len(response['items'])):
                if response['items'][i]['id'].get('channelId') is not None:
                    channel_ids.append(response['items'][i]['id'].get('channelId'))

            next_page_token = response.get('nextPageToken')

            if next_page_token is None:
                break

        return channel_ids

    def search_playlist_ids(self, keyword) -> list:

        playlist_ids = []
        next_page_token = None

        while True:

            try:
                request = self.youtube.search().list(
                    part="snippet",
                    maxResults=50,
                    q=keyword,
                    type="playlist",
                    pageToken=next_page_token)

                response = request.execute()

            except Exception as ex:
                print("Error in making response in search_playlist_ids", ex)
                return None

            for i in range(len(response['items'])):
                if response['items'][i]['id'].get('playlistId') is not None:
                    playlist_ids.append(response['items'][i]['id'].get('playlistId'))

            next_page_token = response.get('nextPageToken')

            if next_page_token is None:
                break

        return playlist_ids


    def search_videos(self, keyword) -> list:

        video_ids = self.search_video_ids(keyword)

        videos_detail = self.get_videos_detail(video_ids)

        return videos_detail


    def search_playlists(self, keyword) -> list:

        playlist_ids = self.search_playlist_ids(keyword)

        playlists_detail = self.get_playlists_detail(playlist_ids)
        return playlists_detail


    def search_channels(self, keyword) -> list:

        channel_ids = self.search_channel_ids(keyword)
        all_channel_data = []

        for channel_id in channel_ids[:4]:

            channel_data = self.get_channel_detail(channel_id)

            data = dict(channel_id=channel_id,
                        channel_detail=channel_data)

            all_channel_data.append(data)

        return all_channel_data


# channel_satistics = get_channel_detail(["UCGaYiIpVOEzUWWS9A1zrodQ"])
# print(channel_satistics)

# video_ids = get_video_ids("UUfM3zsQsOnfWNUppiycmBuw")
# print(video_ids)

# video_details = get_videos_detail(video_ids)
# print(video_details)

# channel_playlists = get_channel_playlists("UCfM3zsQsOnfWNUppiycmBuw")
# print(channel_playlists)

# video = search_videos("eminem")
# print(video)

# channels = search_channels("eminem")
# print(channels)

# playlists = search_playlist("eminem")
# print(playlists)

from googleapiclient.discovery import build

API_KEY = "AIzaSyB-DN3bTPNC5fnfBEcEXQurycWKshVFgOo"
CHANNEL_IDS = ["UCGaYiIpVOEzUWWS9A1zrodQ"]

youtube = build('youtube', 'v3', developerKey=API_KEY)

def get_channel_detail():

    all_data = []

    request = youtube.channels().list(
        part='snippet, contentDetails, statistics',
        id=','.join(CHANNEL_IDS))

    response = request.execute()

    for i in range(len(response['items'])):

        playlist_details = get_channel_playlists(channel_id=response['items'][i]['id'])
        all_videos = get_videos_detail(get_video_ids(response['items'][i]['contentDetails']['relatedPlaylists']['uploads']))

        data = dict(channel_name=response['items'][i]['snippet']['title'],
                    channel_id=response['items'][i]['id'],
                    playlist_id=response['items'][i]['contentDetails']['relatedPlaylists']['uploads'],
                    subscriber_count=response['items'][i]['statistics']['subscriberCount'],
                    total_views=response['items'][i]['statistics']['viewCount'],
                    total_videos=response['items'][i]['statistics']['videoCount'],
                    logo_url=response['items'][i]['snippet']['thumbnails']['medium']['url'],
                    published_date=response['items'][i]['snippet']['publishedAt'],
                    channel_desc=response['items'][i]['snippet']['description'],
                    all_playlists=playlist_details,
                    all_videos= all_videos)

        all_data.append(data)

    return all_data


def get_video_ids(playlist_id):

    video_ids = []
    next_page_token = None

    while True:

        request = youtube.playlistItems().list(
            part='contentDetails',
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token)

        response = request.execute()

        for i in range(len(response['items'])):
            video_ids.append(response['items'][i]['contentDetails']['videoId'])

        next_page_token = response.get('nextPageToken')

        if next_page_token is None:
            break

    return video_ids


def get_videos_detail(video_ids):

    all_video_stats = []

    for i in range(0, len(video_ids), 50):

        request = youtube.videos().list(
                    part='snippet,statistics,id',
                    id=','.join(video_ids[i:i+50]))

        response = request.execute()

        for video in response['items']:

            video_stats = dict(
                 title=video['snippet']['title'],
                 channel_id=video['snippet']['channelId'],
                 view_count=video['statistics'].get('viewCount'),
                 like_count=video['statistics'].get('viewCount'),
                 comment_count=video['statistics'].get('commentCount'),
                 published_date=video['snippet']['publishedAt'],
                 video_thumbnail_url=video['snippet']['thumbnails']['medium']['url'],
                 video_desc=video['snippet']['description'])

            all_video_stats.append(dict(video_id={ video['id']: video_stats}))

    return all_video_stats

def get_channel_playlists(channel_id):

    all_playlists = []
    next_page_token = None

    while True:

        request = youtube.playlists().list(
            part='id,snippet, contentDetails',
            channelId=channel_id,
            maxResults=50,
            pageToken=next_page_token)

        response = request.execute()

        for i in range(len(response['items'])):

            playlist_videos = get_videos_detail(get_video_ids(response['items'][i]['id']))

            playlist = dict(
                playlist_title=response['items'][i]['snippet']['title'],
                playlist_id=response['items'][i]['id'],
                item_count=response['items'][i]['contentDetails']['itemCount'],
                playlist_thumbnail_url=response['items'][i]['snippet']['thumbnails']['medium']['url'],
                playlist_desc=response['items'][i]['snippet']['description'],
                playlist_vidoes=playlist_videos)

            all_playlists.append(playlist)

        next_page_token = response.get('nextPageToken')
        if next_page_token is None:
            break

    return all_playlists



def search(keyword):

    video_ids = []
    next_page_token = None

    while True:

        request = youtube.search().list(
            part="snippet",
            q=keyword,
            maxResults=50,
            pageToken=next_page_token)

        response = request.execute()

        for i in range(len(response['items'])):
            video_id = response['items'][i]['id'].get('videoId')
            if video_id is not None:
                video_ids.append(video_id)

        next_page_token = response.get('nextPageToken')

        if next_page_token is None:
            break

    print(video_ids)
    print(get_videos_detail(video_ids))





channel_satistics = get_channel_detail()
print(channel_satistics)

# video_ids = get_video_ids("UUfM3zsQsOnfWNUppiycmBuw")
# print(video_ids)
#
# video_details = get_videos_detail(video_ids)
# print(video_details)

# channel_playlists = get_channel_playlists("UCfM3zsQsOnfWNUppiycmBuw")
# print(channel_playlists)

# data = search("eminem")
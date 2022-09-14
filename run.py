from src.main import Scrapper

obj= Scrapper()
#
# channel_data=obj.get_channel_detail("UCGaYiIpVOEzUWWS9A1zrodQ")
# print(channel_data)

# videos_data = obj.search_videos("ciber crime 2020")
# print(videos_data)

# playlists_data = obj.search_playlists("best animation movies")
# print(playlists_data)

channels_data = obj.search_channels("doremon")
print(channels_data)
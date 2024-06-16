import os
from dotenv import load_dotenv

# Regex for parsing
import re

# Google API
from googleapiclient.discovery import build

load_dotenv('google.env')
api_key: str = os.getenv('GOOGLE_API_KEY')

youtube = build('youtube', 'v3', developerKey=api_key)


def convert_iso8601_to_seconds(duration: str) -> int:
    """
    Converts an ISO 8601 duration string to seconds.

    Args:
        duration: The ISO 8601 duration string (e.g., "P1DT2H3M4S").

    Returns:
        The duration in seconds.
    """

    time_extractor = re.compile(r"^PT([0-9]*DT)?([0-9]*H)?([0-9]*M)?([0-9]*S)?$", re.I)
    extracted = time_extractor.match(duration)

    if extracted:
        days = 0 if not extracted.group(1) else int(extracted.group(1)[:-2])
        hours = 0 if not extracted.group(2) else int(extracted.group(2)[:-1])
        minutes = 0 if not extracted.group(3) else int(extracted.group(3)[:-1])
        seconds = 0 if not extracted.group(4) else int(extracted.group(4)[:-1])
        return (
                days * 24 * 60 * 60
                + hours * 60 * 60
                + minutes * 60
                + seconds
        )
    print("Error Extracting time")
    return 0


def get_video_ids(playlist_id):
    """
    Get list of video IDs of all videos in the given playlist.

    Args:
        playlist_id (str): YouTube playlist ID.

    Returns:
        List[str]: List of video IDs of all videos in the playlist.
    """
    video_ids = []
    request = youtube.playlistItems().list(
        part='contentDetails',
        playlistId=playlist_id,
        maxResults=50  # Max allowed by API
    )
    while request:
        response = request.execute()
        video_ids += [item['contentDetails']['videoId'] for item in response['items']]
        request = youtube.playlistItems().list_next(request, response)

    return video_ids


def get_video_details(video_ids):
    """
    Get video statistics of all videos with given IDs.

    Args:
        video_ids (List[str]): List of video IDs.

    Returns:
        DataFrame: DataFrame with title and duration of the videos.
    """
    all_video_info = []
    for i in range(0, len(video_ids), 50):  # API allows max 50 IDs at once
        ids_segment = ','.join(video_ids[i:i + 50])
        request = youtube.videos().list(
            part="snippet,contentDetails",
            id=ids_segment
        )
        response = request.execute()
        for video in response['items']:
            video_info = {
                'video_id': video['id'],
                'title': video['snippet']['title'],
                'duration': video['contentDetails']['duration']
            }
            all_video_info.append(video_info)
    return all_video_info


if __name__ == '__main__':
    print(api_key)

    # p_id = 'PLI_7Mg2Z_-4KU0S6_qMAojurEZ2C__j8w'
    # v_ids = get_video_ids(p_id)
    # videos_df = get_video_details(v_ids)
    # for item in videos_df:
    #     item['durationSecs'] = convert_iso8601_to_seconds(item['duration'])
    # print(f'{videos_df[0].keys()}', end='\n\n')
    # # iterate through rows of the dataframe
    # for item in videos_df[:5]:
    #     print(item['title'], item['durationSecs'])

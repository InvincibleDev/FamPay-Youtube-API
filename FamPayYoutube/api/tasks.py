import os
import requests
from datetime import datetime, timedelta

from django.conf import settings
from celery import shared_task, current_task

from api.models import Video, ApiToken


@shared_task
def get_youtube_videos():
    '''
    # TODO: docstring
    '''
    url = "https://youtube.googleapis.com/youtube/v3/search/"
    interval = 50 # 50 seconds interval before querying again
    nextPageToken = ""

    query_params = {
        "part":"snippet",
        "maxResults":100,
        "order":"date",
        "publishedAfter":(datetime.utcnow()-timedelta(seconds=interval)).isoformat().split(".")[0]+"Z",
        "q":"football",
        "type":"video",
        "pageToken":nextPageToken,
        "key":"",
    }

    while nextPageToken != None:

        key_object = ApiToken.objects.filter(is_exhausted = False)
        if key_object.count() < 1:
            current_task.update_state(state='FAILED', meta={'MESSAGE': "ADD MORE API KEYS"})
            return "FAILED"
        api_key = key_object[0]
        query_params["key"] = api_key.token

        video_data_list = []

        response = requests.get(url = url, params = query_params)

        if response.status_code == 403 or response.status_code == 429:
            api_key.is_exhausted = True
            api_key.save()
            continue

        if response.status_code == 200:
            data = response.json()
            nextPageToken = data.get("nextPageToken")
            query_params["pageToken"] = nextPageToken

            retrived_video_list = data.get("items")

            if not retrived_video_list:
                return "SUCCESS"

            for video in retrived_video_list:
                video_data_list.append(Video(
                    video_id = video.get('id').get('videoId'),
                    title =  video.get('snippet').get('title'),
                    description = video.get('snippet').get('description'),
                    published_date = video.get('snippet').get('publishTime'),
                    thumbnail_url = video.get('snippet').get('thumbnails').get('default').get('url'),
                ))

            Video.objects.bulk_create(video_data_list, ignore_conflicts=True)
        else:
            return "FAILED"
    return "SUCCESS"

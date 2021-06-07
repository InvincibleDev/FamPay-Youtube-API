import os
import requests
from datetime import datetime, timedelta

from django.conf import settings
from celery import shared_task, current_task

from api.models import Video, ApiToken


@shared_task
def get_youtube_videos():
    """
    Scheduled task to run every 50 seconds to load new videos from youtube search API.
    Topic Choosen = "Football"
    """
    url = "https://youtube.googleapis.com/youtube/v3/search/"
    interval = 50 # 50 seconds interval before querying again
    nextPageToken = ""

    query_params = {
        "part":"snippet",
        "maxResults":100,
        "order":"date",
        "publishedAfter":(datetime.utcnow()-timedelta(seconds=interval)).isoformat().split(".")[0]+"Z", #load new videos posted in the previous interval
        "q":"football",
        "type":"video",
        "pageToken":nextPageToken,
        "key":"",
    }

    while nextPageToken != None:

        # Check for API Keys that are not exhausted already and use them.
        key_object = ApiToken.objects.filter(is_exhausted = False)
        if key_object.count() < 1:
            current_task.update_state(state='FAILED', meta={'MESSAGE': "ADD MORE API KEYS"}) # Fail task if all API Keys are exhausted
            return "FAILED"
        api_key = key_object[0]
        query_params["key"] = api_key.token  # set API Key

        video_data_list = []

        response = requests.get(url = url, params = query_params)

        # Check if API Key is exhausted and take action
        if response.status_code == 403 or response.status_code == 429:
            api_key.is_exhausted = True
            api_key.save()
            continue

        # If API request is successful
        if response.status_code == 200:
            data = response.json()

            # if pagination is provoided by Youtube search API
            nextPageToken = data.get("nextPageToken")
            query_params["pageToken"] = nextPageToken

            retrived_video_list = data.get("items") # Load video items

            if not retrived_video_list: # If no new videos are posted
                return "SUCCESS"

            # Bulk Create all videos data
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

@shared_task
def enable_api_keys():
    """
    Scheduled task to run every 24 hours to enable all API Keys in DB
    """
    qs = ApiToken.objects.all()
    qs.update(is_exhausted=False)
    return "SUCCESS"

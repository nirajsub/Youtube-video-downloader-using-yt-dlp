from django.shortcuts import render, redirect
import os
from django.http.response import HttpResponseRedirect, JsonResponse
import requests
from django.http import HttpResponse
import youtube_dl
import yt_dlp
from yt_dlp import YoutubeDL
import json
import re
from yt_dlp.utils import DownloadError

class MyCustomPP(yt_dlp.postprocessor.PostProcessor):
    def run(self, info):
        self.to_screen('Youtube Video Downloader')
        return [], info

def user_sanitize_info(info):
    user_dict = {
        'video_id': [],
        'videoid': [],
        'audio_formats': [],
        'video_formats': [],
        'title': info['title'],
        'thumbnail': info['thumbnail'],
        'duration': info['duration_string']
    }
    for formats in info['formats']:
        if 'none' in formats['video_ext'] and 'none' != formats['audio_ext']:
            file_size = formats['filesize'] if formats["filesize"]!=None else formats["filesize_approx"]
            if file_size is not None:
                if file_size > 1000000000:
                    file_size = f'{round(int(file_size) / 1000000000,2)} GB'
                else:
                    file_size = f'{round(int(file_size) / 1000000,2)} MB'
            user_dict['audio_formats'].append(
                {
                    'format_name': formats['format'],
                    'abr': str(int(formats["abr"])) + " Kbps",
                    'audio_ext': formats['audio_ext'],
                    'audio_filesize': file_size,
                    'url': formats['url']
                }
            )
        if 'none' in formats['audio_ext'] and 'none' != formats['video_ext']:
            file_size = formats['filesize'] if formats["filesize"]!=None else formats["filesize_approx"]
            if file_size is not None:
                if file_size > 1000000000:
                    file_size = f'{round(int(file_size) / 1000000000,2)} GB'
                else:
                    file_size = f'{round(int(file_size) / 1000000,2)} MB'
            user_dict['video_formats'].append(
                {
                    'format_name': formats['format'],
                    'acodec': formats['acodec'],
                    'format_note': formats['format_note'],
                    'video_ext': formats['video_ext'],
                    'video_filesize': file_size,
                    'url': formats['url'],
                    'resolution': formats["resolution"].split("x")[1]
                }
            )
            
    return user_dict

def format_selector(ctx):

    formats = ctx.get('formats')[::-1]

    best_video = next(f for f in formats
                      if f['vcodec'] != 'none' and f['acodec'] == 'none')

    audio_ext = {'mp4': 'm4a', 'webm': 'webm'}[best_video['ext']]
    best_audio = next(f for f in formats if (
        f['acodec'] != 'none' and f['vcodec'] == 'none' and f['ext'] == audio_ext))

    yield {
        'format_id': f'{best_video["format_id"]}+{best_audio["format_id"]}',
        'ext': best_video['ext'],
        'requested_formats': [best_video, best_audio],
        'protocol': f'{best_video["protocol"]}+{best_audio["protocol"]}'
    }

def get_youtube_extract(url: str):
    ydl_opts = {
        'format': format_selector,
        'postprocessors': [{
            'key': 'FFmpegMetadata',
            'add_chapters': True,
            'add_metadata': True,
        }],
    }
    yt_dlp.utils.std_headers.update({'Referer': 'https://www.google.com'})

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.add_post_processor(MyCustomPP())
        info = ydl.extract_info(url, download=False)
        sanitize_info = ydl.sanitize_info(info)
        user_sanitize = user_sanitize_info(sanitize_info)
        return user_sanitize

def index(request):
    if 'POST' in request.method:
        video_url = request.POST.get('urls')
        if 'watch' in video_url:
            video_url = video_url
            video_id = video_url.split("=")[-1]
            video_url = ('https://www.youtube.com/watch?v=' + (video_id))
            regex = r'^(http(s)?:\/\/)?((w){3}.)?youtu(be|.be)?(\.com)?\/.+'
            if re.match(regex, video_url):
                user_dict = get_youtube_extract(video_url)
                user_dict['video_formats'] = user_dict['video_formats'][::-1]
                context = {
                                    'video_title': user_dict['title'],
                                    'thumbnail': user_dict['thumbnail'],
                                    'duration': user_dict['duration'],
                                    'video_dict': user_dict['video_formats'],
                                    'audio_dict': user_dict['audio_formats'],
                                    'video_id': video_id
                }
        elif 'shorts' in video_url:
            video_url = video_url.replace('shorts/', 'watch?v=')
            videoid = video_url.split("=")[-1]
            video_id = video_url.split("=")[-1]
            print("VIDEO_ID:", video_id)
            video_url = ('https://www.youtube.com/watch?v=' + (video_id))
            print("VIDEO_URL:", video_url)
            regex = r'^(http(s)?:\/\/)?((w){3}.)?youtu(be|.be)?(\.com)?\/.+'
            if re.match(regex, video_url):
                user_dict = get_youtube_extract(video_url)
                user_dict['video_formats'] = user_dict['video_formats'][::-1]
                context = {
                                    'video_title': user_dict['title'],
                                    'thumbnail': user_dict['thumbnail'],
                                    'duration': user_dict['duration'],
                                    'video_dict': user_dict['video_formats'],
                                    'audio_dict': user_dict['audio_formats'],
                                    'videoid': videoid
                }
        else:
            error1= ("Please enter a valid URL!")
            return render(request, 'index.html', {'error1': error1})
        return render(request, 'index.html', context)  
    return render(request, 'index.html')

def SetLanguage(request, lang):
    if request.method == "GET":
        lang = request.GET.get('lang')

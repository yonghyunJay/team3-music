from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from .util import random_album_img_urls, get_album_img_urls_to_list, current_album_img_urls, random_song_name
from .recommend_model import dummy_func
from django.views.decorators.csrf import csrf_exempt
import json

def index(request):
    template = loader.get_template('musicApp/index.html')
    context = {
        'latest_question_list': "test",
    }
    temp = []
    res_dict = random_song_name(temp, 10)
    return render(request, 'musicApp/index.html', {'res_dict' : res_dict})

def get_recommend_music(request):
    if request.method == 'POST':
        recv_list = request.POST.getlist('nameList[]')
    
        response_data = {}
        outputList = dummy_func(recv_list)
        
        response_data['name'] = outputList
        response_data['album_img_url'] = get_album_img_urls_to_list(outputList)

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

def update_list(request):
    if request.method == 'POST':
        recv_list = request.POST.getlist('nameList[]')
        # print("0.",  recv_list)
        response_data = {}
        
        nameTemp = []
        urlTemp = []
        selected = []

        outputList = current_album_img_urls(recv_list)

        for key, value in outputList.items():
            # print("1. ", key, ":", value)
            nameTemp.append(value['song_name'])
            urlTemp.append(value['img_url'])
            selected.append(1)

        outputList = random_album_img_urls(recv_list, 10)

        for key, value in outputList.items():
            # print("2. ", key, ":", value)
            nameTemp.append(value['song_name'])
            urlTemp.append(value['img_url'])
            selected.append(0)
        
        response_data['name'] = nameTemp
        response_data['album_img_url'] = urlTemp
        response_data['selected'] = selected

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

from django.http import HttpResponse
from django.shortcuts import render, reverse
from datetime import datetime
from os import listdir
from app.create_html import create_html


def home_view(request):
    template_name = 'app/home.html'

    pages = {
        'Главная страница': reverse('home'),
        'Показать текущее время': reverse('time'),
        'Показать содержимое рабочей директории': reverse('workdir'),
        'Видео': reverse('video')
    }

    context = {
        'pages': pages
    }
    return render(request, template_name, context)


def time_view(request):
    current_time = str(datetime.now().time())[0:5]
    msg = f'Текущее время: {current_time}'
    page = create_html(f'<p>{msg}</p>')
    return HttpResponse(page)


def workdir_view(request):
    dirs = ''.join([f'<li>{file}</li>' for file in listdir()])
    page = create_html(f'<ul>{dirs}</ul>')
    return HttpResponse(page)

def video_view(request):
    video_html = '''
    <iframe width="560" height="315" src="https://www.youtube.com/embed/K-eada1juAY" 
    title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; 
    clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
    '''
    page = create_html(video_html)
    return HttpResponse(page)
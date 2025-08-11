from django.http import HttpResponse
from django.shortcuts import render, reverse
from datetime import datetime
import os


def home_view(request):
    """Функция возвращает список доступных страниц"""

    template_name = 'app/home.html'
    pages = {
        'Главная страница': reverse('home'),
        'Показать текущее время': reverse('time'),
        'Показать содержимое рабочей директории': reverse('workdir')
    }
    
    # context и параметры render менять не нужно
    # подбробнее о них мы поговорим на следующих лекциях
    context = {
        'pages': pages
    }
    return render(request, template_name, context)


def time_view(request):
    """Функция возвращает текущее время формате Часы:Минуты"""

    current_time = datetime.now().strftime("%H:%M")
    msg = f'Текущее время: {current_time}'
    return HttpResponse(msg)


def workdir_view(request):
    """Функция возвращает список файлов в текущей директории"""

    current_dir = os.getcwd()
    contents = os.listdir(current_dir)
    files = []
    for item in contents:
        if os.path.isfile(item):
            files.append(item)
    output = (f'Текущая директория: {current_dir} '
              f'содержит файлы:<br/> {"<br/>".join(files)}')
    return HttpResponse(output)

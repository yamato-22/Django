from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
import csv


def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    # получите текущую страницу и передайте ее в контекст
    # также передайте в контекст список станций на странице
    CONTENT: list = []
    with open(settings.BUS_STATION_CSV, mode="r", encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            CONTENT.append(row)

    paginator = Paginator(CONTENT, 10)
    page_number = int(request.GET.get('page', 1))
    page = paginator.get_page(page_number)
    context = {
        'page': page,
    }
    return render(request, 'stations/index.html', context)

from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from requests.compat import quote_plus
from . import models

BASE_LISTA_URL = 'http://www.listademaestros.com/fime/buscar/{}'

# Create your views here.
def home(request):
    return render(request, 'base.html')

def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)

    search = search.replace(' ', '-')
    final_url = BASE_LISTA_URL.format(search)
    
    # print(search)
    # print(data)
    # print(final_url)
    stuff_for_frontend = {
        'search': search,
        }

    return render(request, 'maestros_app/newsearch.html', stuff_for_frontend)
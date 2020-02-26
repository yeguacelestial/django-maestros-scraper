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
    
    response = requests.get(final_url)
    data = response.text

    soup = BeautifulSoup(data, features='html.parser')

    # Maestros listing
    maestros_list = soup.find_all('td', {'class': 'results_left_td'})
    
    # # Nombre del maestro
    # maestro_name = maestros_list[1].a.text
    
    # # Link del maestro
    # maestro_link = maestros_list[1].a.get('href')
    
    # # Chidos y gachos
    # chidos = maestros_list[1].find(class_="result_chido_score").text
    # gachos = maestros_list[1].find(class_="result_gacho_score").text

    # Final postings
    final_postings = []

    for maestro in maestros_list[1:]:
        maestro_name = maestro.a.text
        maestro_link = maestro.a.get('href')
        chidos = maestro.find(class_="result_chido_score").text
        gachos = maestro.find(class_="result_gacho_score").text

        final_postings.append((maestro_name, maestro_link, chidos, gachos))
    
    search = search.replace('-', ' ')
    
    stuff_for_frontend = {
        'search': search,
        'final_postings': final_postings,
        }

    return render(request, 'maestros_app/newsearch.html', stuff_for_frontend)
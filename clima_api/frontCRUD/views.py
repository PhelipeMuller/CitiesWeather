from django.shortcuts import render, redirect
from .models import City
from .forms import CityForm
import requests

# Create your views here.

def list_cities(request):
    url = "http://127.0.0.1:8000/v1/cities"
    payload = ""
    headers = {
        'cache-control': "no-cache"
    }
    response = requests.request("GET", url, data=payload, headers=headers)
    cities = []
    for r in response.json():
        cities.append(Struct(**r))
    return render(request, 'cities.html', {'cities': cities})

def search_city(request):
    form = CityForm(request.POST or None)


    if form.is_valid():
        url = "http://127.0.0.1:8000/v1/city/{0}".format(form.cleaned_data['name'])

        payload = ""
        headers = {
            'cache-control': "no-cache"
            }

        response = requests.request("GET", url, data=payload, headers=headers)
        return redirect('List_of_Cities')

    return render(request, 'cities-form.html', {'form': form})

def delete_city(request, name):
    url = "http://127.0.0.1:8000/v1/city/{0}".format(name)

    payload = ""
    headers = {
        'cache-control': "no-cache"
    }

    response = requests.request("DELETE", url, data=payload, headers=headers)
    return redirect('List_of_Cities')

class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)

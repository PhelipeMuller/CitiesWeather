from django.shortcuts import render, redirect
from .models import City
from .forms import CityForm

# Create your views here.

def list_cities(request):
    cities = City.objects.all()
    return render(request, 'cities.html', {'cities': cities})

def search_city(request):
    form = CityForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('List_of_Cities')

    return render(request, 'cities-form.html', {'form': form})

def update_city(request, id):
    city = City.objects.get(id=id)
    form = CityForm(request.POST or None, instance=city)

    if form.is_valid():
        form.save()
        return redirect('List_of_Cities')

    return render(request, 'cities-form.html', {'form': form, 'city': city})


def delete_city(request, id):
    city = City.objects.get(id=id)

    if request.method == 'POST':
        city.delete()
        return redirect('List_of_Cities')

    return render(request, 'delete_city.html', {'city': city})

from django.shortcuts import render
from django.utils import timezone
from rest_framework.views import APIView
from .models import CityWeather
from .serializer import CitySerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
import requests

# Create your views here.

class CityListView(APIView):
    parser_classes = (MultiPartParser, FormParser,)
    serializer_class = CitySerializer

    def get(self, request, format=None):
        cities = CityWeather.objects.all()
        serializer = CitySerializer(cities, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"messagem": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class CityView(APIView):
    serializer_class = CitySerializer

    def get(self, request, name):
        try:
            city = CityWeather.objects.get(name=name)
        except:
            getFromFather(name)
            city = CityWeather.objects.get(name=name)
        serializer = self.serializer_class(city)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, name, format=None):
        city = CityWeather.objects.get(name=name)
        serializer = self.serializer_class(city, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, name, format=None):
        try:
            city = CityWeather.objects.get(name=name)
            city.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as message:
            return Response(status=status.HTTP_404_NOT_FOUND)

def getFromFather(name):
    url = 'http://api.openweathermap.org/data/2.5/forecast?q='+name+'&APPID=70de57c90172d1d186f1842ef7a082c2'
    payload = ""
    headers = {
            'cache-control': "no-cache"
    }
    response = requests.request("GET", url, data=payload, headers=headers)

    flag = 1
    cnt = 0
    fahrenheit = 0
    rain = 0
    while(flag):
        if(response.json().get('list')[cnt]['dt_txt'].split(" ")[0]==str(timezone.now().date())):
            fahrenheit += int(response.json().get('list')[cnt]['main']['temp'])
            if (response.json().get('list')[cnt]['weather'][0]['main']=='Rain'):  rain+=3
            cnt+=1
        else:
            flag = 0
            print(cnt)
            fahrenheit /= cnt
            celcius = fahrenheitToCelcius(fahrenheit)
            url = "http://127.0.0.1:8000/v1/cities"

            payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"name\"\r\n\r\n{0}\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"celcius\"\r\n\r\n{1}\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"time_rain\"\r\n\r\n{2}\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--".format(name,celcius,rain)
            headers = {
                'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
                'cache-control': "no-cache"
            }
            print(payload)
            response = requests.request("POST", url, data=payload, headers=headers)
            print(response.text)

def fahrenheitToCelcius(f):
    return int((f-32)*(5/18))

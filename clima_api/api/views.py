from django.shortcuts import render
from rest_framework.views import APIView
from .models import CityWether
from .serializer import CitySerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

# Create your views here.

class CityListView(APIView):
    parser_classes = (MultiPartParser, FormParser,)
    serializer_class = CitySerializer

    def get(self, request, format=None):
        cities = CityWether.objects.all()
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

    def get(self, request, pk):
        city = CityWether.objects.get(pk=pk)
        serializer = self.serializer_class(city)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        city = CityWether.objects.get(pk=pk)
        serializer = self.serializer_class(city, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        try:
            city = CityWether.objects.get(pk=pk)
            city.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as message:
            return Response(status=status.HTTP_404_NOT_FOUND)

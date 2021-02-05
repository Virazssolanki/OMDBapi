from django.shortcuts import render, redirect
from .serializers import MovieSerializer
from .filters import MovieFilter
from .models import Movie, Ratings
from .forms import SearchForm
from django.db.models import Q
import requests
import json

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework import generics

class MovieView(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


def search(request):
    movies = Movie.objects.all()
    movie_filter = MovieFilter(request.GET, queryset=movies)
    return render(request, 'api/movies.html', {'filter': movie_filter})

def find(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            if Movie.objects.filter(title=title).exists():
                movies = Movie.objects.filter(title__iexact=title)
                context = locals()
                return render(request, 'api/home.html', context)
            else:
                url = 'http://www.omdbapi.com/?t=' + title + '&apikey=caeea4d0'
                response = requests.get(url)
                movie_data = response.json()
                r_objs = []
                for rate in movie_data['Ratings']:
                    r, created = Ratings.objects.get_or_create(source=rate['Source'], rating=rate['Value'])
                    r_objs.append(r)
                m, created = Movie.objects.get_or_create(title=movie_data['Title'],year=movie_data['Year'],)
                m.rating.set(r_objs)
                m.save()
                movies = Movie.objects.filter(title=title)
                context = locals()
                return render(request, 'api/home.html', context)
    else:
        form = SearchForm()
        context = locals()
        return render(request, 'api/home.html', context)


@api_view(['GET','POST'])
def m_list(request):
    if request.method == 'GET':
        movies = Movie.objects.all()
        serializers = MovieSerializer(movies,many=True)
        return Response(serializers.data)

    elif(request.method == 'POST'):
        serializers = MovieSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data,status=status.HTTP_201_CREATED)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)

from django.urls import path, include
# from .views import movie_list, movie_detail
from .views import MovieListAV, MovieDetailsAV

urlpatterns = [
    path('list/', MovieListAV.as_view(), name='movie-list'),
    path('<int:movie_id>', MovieDetailsAV.as_view(), name='movie-detail'),
]
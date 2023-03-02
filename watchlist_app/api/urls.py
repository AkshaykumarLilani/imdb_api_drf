from django.urls import path, include
# from .views import movie_list, movie_detail
from .views import WatchListAV, WatchListDetailsAV, StreamPlatformListAV, StreamPlatformDetailView, ReviewListGv, ReviewDetailGv

urlpatterns = [
    path('list/', WatchListAV.as_view(), name='watchlist'),
    path('<int:watchlist_id>', WatchListDetailsAV.as_view(), name='watchlist-details'),
    path('streamingplatform/list', StreamPlatformListAV.as_view(), name='streamplatforms-list'),
    path('streamingplatform/<int:stream_platform_id>', StreamPlatformDetailView.as_view(), name='streamplatforms-list'),
    path('reviews/', ReviewListGv.as_view(), name='review-list'),
    path('reviews/<int:pk>', ReviewDetailGv.as_view(), name='review-list')
]
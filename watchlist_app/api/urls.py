from django.urls import path, include
# from .views import movie_list, movie_detail
# from .views import ReviewListGv, ReviewDetailGv
from .views import WatchListAV, WatchListDetailsAV, StreamPlatformListAV, StreamPlatformDetailView, ReviewList, ReviewDetail, ReviewCreate

urlpatterns = [
    path('list/', WatchListAV.as_view(), name='watchlist'),
    path('<int:watchlist_id>', WatchListDetailsAV.as_view(), name='watchlist-details'),
    path('streamingplatform/list', StreamPlatformListAV.as_view(), name='streamplatforms-list'),
    path('streamingplatform/<int:stream_platform_id>', StreamPlatformDetailView.as_view(), name='streamplatforms-list'),
    
    path('streamingplatform/<int:pk>/review-create', ReviewCreate.as_view(), name='review-create'),
    path('streamingplatform/<int:pk>/reviews', ReviewList.as_view(), name='review-list'),
    path('streamingplatform/reviews/<int:pk>', ReviewDetail.as_view(), name='review-list'),
    
    # path('reviews/', ReviewListGv.as_view(), name='review-list'),
    # path('reviews/<int:pk>', ReviewDetailGv.as_view(), name='review-list')
]
from django.urls import path, include
# from .views import movie_list, movie_detail
# from .views import ReviewListGv, ReviewDetailGv
from .views import WatchListAV, WatchListDetailsAV, StreamPlatformListAV, StreamPlatformDetailView, ReviewList, ReviewDetail, ReviewCreate, StreamPlatformVs
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('streamingplatform', StreamPlatformVs, basename='streamplatform')

urlpatterns = [
    path('list/', WatchListAV.as_view(), name='watchlist'),
    path('<int:watchlist_id>/', WatchListDetailsAV.as_view(), name='watchlist-details'),
    
    path('',include(router.urls)),
    
    # path('streamingplatform/list', StreamPlatformListAV.as_view(), name='streamplatforms-list'),
    # path('streamingplatform/<int:stream_platform_id>', StreamPlatformDetailView.as_view(), name='streamplatforms-list'),
    
    path('<int:pk>/review-create', ReviewCreate.as_view(), name='review-create'),
    path('<int:pk>/reviews', ReviewList.as_view(), name='review-list'),
    path('reviews/<int:pk>', ReviewDetail.as_view(), name='review-list'),
    
    # path('reviews/', ReviewListGv.as_view(), name='review-list'),
    # path('reviews/<int:pk>', ReviewDetailGv.as_view(), name='review-list')
]
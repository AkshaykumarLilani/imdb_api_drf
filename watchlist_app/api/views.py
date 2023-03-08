from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, viewsets
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
# from rest_framework.decorators import api_view
from rest_framework.permissions import IsAdminUser
from .permissions import AdminOrReadOnly, ReviewUserOrReadOnly

from django.shortcuts import get_object_or_404

from watchlist_app.models import WatchList, StreamPlatforms, Review
from .serializers import WatchListSerializer, StreamPlatformsSerializer, ReviewSerializer
# from rest_framework import mixins

class StreamPlatformVs(viewsets.ModelViewSet):
    queryset = StreamPlatforms.objects.all()
    serializer_class = StreamPlatformsSerializer
    
# class StreamPlatformVs(viewsets.ViewSet):
    
#     def list(self, request):
#         queryset = StreamPlatforms.objects.all()
#         serializer = StreamPlatformsSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def retrieve(self, request, pk=None):
#         queryset = StreamPlatforms.objects.all()
#         watchlist = get_object_or_404(queryset, pk=pk)
#         serializer = StreamPlatformsSerializer(watchlist)
#         return Response(serializer.data)

class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        return Review.objects.all()
    
    def perform_create(self, serializer):
        pk = self.kwargs['pk']
        watchlist = WatchList.objects.get(pk=pk)
        
        review_user_ = self.request.user
        review_queryset = Review.objects.filter(watchlist=watchlist, review_user=review_user_)
        
        if review_queryset.exists():
            raise ValidationError("You have already reviewed this watchlist")

        if watchlist.number_of_ratings == 0:
            watchlist.avg_rating = serializer.validated_data['rating']
        else:
            watchlist.avg_rating = (watchlist.avg_rating + serializer.validated_data['rating'])/2
            
        watchlist.number_of_ratings = watchlist.number_of_ratings + 1;
        watchlist.save()
        
        serializer.save(watchlist=watchlist, review_user=review_user_)

class ReviewList(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAdminUser]
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)
    

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [ReviewUserOrReadOnly]

# class ReviewDetailGv(mixins.RetrieveModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
    
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

# class ReviewListGv(mixins.CreateModelMixin, mixins.ListModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
    
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
    
#     def update(self, request, *args, **kwargs):
#          return self().create(request, *args, **kwargs)

class WatchListAV(APIView):
        
    def get(self, request):
        # 1. Get the complex data
        watchlist = WatchList.objects.all()
        
        # 2. Convert the complex data to python native datatype
        serializer = WatchListSerializer(watchlist, many=True) 
            # if you don't add many=True, then you will get a 'Got AttributeError when attempting to get a value for field `name` on serializer `WatchListSerializer`.The serializer field might be named incorrectly and not match any attribute or key on the `QuerySet` instance. Original exception text was: 'QuerySet' object has no attribute 'name'.
        
        # 3. return the serializer.data to the response function from the rest framework which will automatically convert the native datatype to json
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # the serializer.data comes from def create method written in the serializer
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WatchListDetailsAV(APIView):
    
    def get(self, request, watchlist_id):
        
        try:
            movie = WatchList.objects.get(pk=watchlist_id)
        except WatchList.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = WatchListSerializer(movie)
            # You don't need to add many=True, because here we are accessing only one object not many objects at once.
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self ,request, watchlist_id):
        #1. First fetch the movie which is to be updated.
        try:
            movie = WatchList.objects.get(pk=watchlist_id)
        except WatchList.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        #2. Pass the movie which is to be updated to the serializer and the new data to update with it. This will go to serializer and hit the update method which we wrote there and will bring whatever the update method returns.
        serializer = WatchListSerializer(movie, data=request.data)
        #3. check if the serializer is valid and save if it is or send errors if it is not.
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, watchlist_id):
        #1. First fetch the movie which is to be deleted.
        try:
            movie = WatchList.objects.get(pk=watchlist_id)
        except WatchList.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        #2. Delete it!
        movie.delete()
        #3. send the response accordingly.
        return Response(status=status.HTTP_204_NO_CONTENT)

class StreamPlatformListAV(APIView):
    
    def get(self, request):
        all_stream_platforms = StreamPlatforms.objects.all()
        serializer = StreamPlatformsSerializer(all_stream_platforms, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = StreamPlatformsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StreamPlatformDetailView(APIView):
    
    def get(self, request, stream_platform_id):
        try:
            stream_platform = StreamPlatforms.objects.get(pk=stream_platform_id)
        except StreamPlatforms.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = StreamPlatformsSerializer(stream_platform)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, stream_platform_id):
        try:
            stream_platform = StreamPlatforms.objects.get(pk=stream_platform_id)
        except StreamPlatforms.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = StreamPlatformsSerializer(stream_platform, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, stream_platform_id):
        try:
            stream_platform = StreamPlatforms.objects.get(pk=stream_platform_id)
        except StreamPlatforms.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        stream_platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
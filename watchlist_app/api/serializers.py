from rest_framework import serializers
from watchlist_app.models import WatchList, StreamPlatforms, Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
class WatchListSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    # what read_only = True means | when i am sending a post request, i am not going to send review. we can only get it when getting it.
    
    class Meta:
        model = WatchList
        fields = '__all__'
        # fields = ['id','name','description'] # show name, id and description field
		# exclude = ['name'] # show all excluding name

class StreamPlatformsSerializer(serializers.ModelSerializer):
    # following will give you all the fields from watchlist
    watchlist = WatchListSerializer(many=True, read_only=True)
    
    # if you want only the field which is returned by __str__ method of the model
    # watchlist = serializers.StringRelatedField(many=True)
    
    # name should be sufficient to explain
    # watchlist = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    # now if you want a hyperlink to the related fields than use following.
    # important thing is the view_name field, it has to be same as the view_name which you provide in the urls to which you want this link to.
    # you will also have to add context={'request': request} in the serializer call of get request in the StreamPlatformListAV view.
    # *** following is throwing an error
    # watchlist = serializers.HyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     view_name='watchlist-details'
    # )
    class Meta:
        model = StreamPlatforms
        fields = '__all__'
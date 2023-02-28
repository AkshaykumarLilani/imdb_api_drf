from rest_framework.response import Response
from rest_framework.decorators import api_view
from watchlist_app.models import Movie
from .serializers import MovieSerializer

# Create your views here.
@api_view(['GET', 'POST']) # GET request is the default one, i.e. if you only write @api_view(), then only GET will be accepted. And because I have written POST here too, I will see a post form when I hit the url to this function.
def movie_list(request):
    
    if request.method == 'GET':
        # 1. Get the complex data
        movies = Movie.objects.all()
        
        # 2. Convert the complex data to python native datatype
        serializer = MovieSerializer(movies, many=True) 
            # if you don't add many=True, then you will get a 'Got AttributeError when attempting to get a value for field `name` on serializer `MovieSerializer`.The serializer field might be named incorrectly and not match any attribute or key on the `QuerySet` instance. Original exception text was: 'QuerySet' object has no attribute 'name'.
        
        # 3. return the serializer.data to the response function from the rest framework which will automatically convert the native datatype to json
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # the serializer.data comes from def create method written in the serializer
            return Response(serializer.data)
        return Response(serializer.errors)

@api_view(['GET', 'PUT', 'DELETE']) # Default is GET request
def movie_detail(request, movie_id):
    if request.method == 'GET':
        movie = Movie.objects.get(pk=movie_id)
        serializer = MovieSerializer(movie)
            # You don't need to add many=True, because here we are accessing only one object not many objects at once.
        return Response(serializer.data)

    if request.method == 'PUT':
        #1. First fetch the movie which is to be updated.
        movie = Movie.objects.get(pk=movie_id)
        #2. Pass the movie which is to be updated to the serializer and the new data to update with it. This will go to serializer and hit the update method which we wrote there and will bring whatever the update method returns.
        serializer = MovieSerializer(movie, data=request.data)
        #3. check if the serializer is valid and save if it is or send errors if it is not.
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    if request.method == 'DELETE':
        #1. First fetch the movie which is to be deleted.
        movie = Movie.objects.get(pk=movie_id)
        #2. Delete it!
        movie.delete()
        #3. send the response accordingly.
        return Response(status=204)

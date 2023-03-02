from rest_framework import serializers
from watchlist_app.models import Movie

# 3. validators
def name_length(value):
    if len(value) < 2:
        raise serializers.ValidationError("Name is too short")
    else:
        return value
    
# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(validators=[name_length])
#     description = serializers.CharField()
#     active = serializers.BooleanField()
        
    
#     def create(self, validated_data):
#         # this return is accessed in serializer.data when serializer.is_valid() returns True in the views
#         return Movie.objects.create(**validated_data)
    
#     #instance carries the old values and validated_data carries the new values
#     def update(self, instance, validated_data):
#         # you have to match all the fields in the validated data with instance and see how the data is accessed from validated_data (we are giving a else field to return if the data is not present in the validated data (instance.name, etc.)).
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get('description', instance.description)
#         instance.active = validated_data.get('active', instance.active)
#         # save it once you have updated all the fields.
#         instance.save()
#         #return the new data to the view
#         return instance

#     # 1. Field level validation.
#     # def validate_name(self, value):
#     #     if len(value) < 2:
#     #         raise serializers.ValidationError("Name is too short")
#     #     else:
#     #         return value
    
#     # 2. object level validation.
#     def validate(self, data):
#         if data["name"] == data["description"]:
#             raise serializers.ValidationError("Name and description cannot be the same")
#         return data

class MovieSerializer(serializers.ModelSerializer):
    name_len = serializers.SerializerMethodField()
    class Meta:
        model = Movie
        fields = '__all__'
        # fields = ['id','name','description'] # show name, id and description field
		# exclude = ['name'] # show all excluding name
  
    def get_name_len(self, object):
        length = len(object.name)
        return length

    # 1. Field level validation.
    def validate_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Name is too short")
        else:
            return value
    
    # 2. object level validation.
    def validate(self, data):
        if data["name"] == data["description"]:
            raise serializers.ValidationError("Name and description cannot be the same")
        return data
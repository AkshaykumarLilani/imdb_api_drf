from django.contrib import admin
from .models import WatchList, StreamPlatforms, Review
# Register your models here.

admin.site.register(WatchList)
admin.site.register(StreamPlatforms)
admin.site.register(Review)
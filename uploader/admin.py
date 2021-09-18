from django.contrib import admin
from .models import OriginalImage, Thumbnail

admin.site.register(OriginalImage)
admin.site.register(Thumbnail)

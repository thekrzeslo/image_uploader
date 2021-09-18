from django.contrib import admin
from .models import SpecialUser, Plan, ThumbnailSize

admin.site.register(SpecialUser)
admin.site.register(Plan)
admin.site.register(ThumbnailSize)
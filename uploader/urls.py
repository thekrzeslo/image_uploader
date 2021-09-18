from django.urls import path, include
from .views import ImageAPI

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('', ImageAPI.as_view(), name='uploader'),
]
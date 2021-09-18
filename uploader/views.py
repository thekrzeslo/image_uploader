from rest_framework import generics
from rest_framework import mixins
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from .serializers import ImageSerializer
from .models import OriginalImage
from account.models import SpecialUser

class CustomPerm(permissions.BasePermission):
    message = 'You do not have a plan yet.'
    def has_permission(self, request, view):
        return SpecialUser.objects.filter(user_id = request.user).exists()

class ImageAPI(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, CustomPerm]
    serializer_class = ImageSerializer
    queryset = OriginalImage.objects.all()

    def perform_create(self, serializer):
        return serializer.save(specialuser_id = SpecialUser.objects.get(user_id = self.request.user))

    def get_queryset(self):
        return self.queryset.filter(specialuser_id = SpecialUser.objects.get(user_id = self.request.user))

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)



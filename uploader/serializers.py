from rest_framework import serializers
from .models import OriginalImage, Thumbnail
from account.models import ThumbnailSize, SpecialUser
from django.db.models import Q

class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = OriginalImage
        fields = ['original_image']

    def to_representation(self, instance):
        representation = super(ImageSerializer, self).to_representation(instance)

        original_image = representation['original_image']

        absolute_url = original_image.replace(instance.original_image.url, '')

        del representation['original_image']

        representation[instance.name] = {}

        for thumbnail_size in ThumbnailSize.objects.all().filter(plan = instance.specialuser_id.plan_id):
            if thumbnail_size.name == 'original':
                representation[instance.name]['original_image'] = original_image

            else:
                obj = Thumbnail.objects.all().filter(Q(image_id=instance.id) & Q(height=thumbnail_size.height))

                if obj.exists():
                    obj = Thumbnail.objects.get(Q(image_id=instance.id) & Q(height=thumbnail_size.height))
                    representation[instance.name][thumbnail_size.name] = f'{absolute_url}{obj.image.url}'

                else:
                    new_thumbnail = Thumbnail(image_id = instance, name=instance.name+'_'+thumbnail_size.name, height=thumbnail_size.height)
                    new_thumbnail.save()
                    representation[instance.name][thumbnail_size.name] = f'{absolute_url}{new_thumbnail.image.url}'

        return representation

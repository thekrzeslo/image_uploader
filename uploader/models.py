from django.db import models
from account.models import SpecialUser
from django.core.validators import FileExtensionValidator
from PIL import Image as PIL_image
from io import BytesIO
from django.core.files import File

def upload_to(instance, filename):
    return f'images/{instance.specialuser_id.user_id.username}/{filename}'

def thumbnail_upload_to(instance, filename):
    image_format = filename.split('.')[-1]
    return f'images/{instance.image_id.specialuser_id.user_id.username}/{instance.name}.{image_format}'


def make_thumbnail(image, height):

    img = PIL_image.open(image)
    new_width  = int(height) * image.width / image.height
    img.thumbnail((new_width, int(height)))

    thumb_io = BytesIO()
    img.save(thumb_io, img.format)
    thumbnail = File(thumb_io, name=image.name)

    return thumbnail

class OriginalImage(models.Model):
    specialuser_id = models.ForeignKey(SpecialUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    original_image = models.ImageField(upload_to=upload_to, validators=[FileExtensionValidator(allowed_extensions=['jpg','png'])])

    def save(self, *args, **kwargs):
        self.name = str(self.original_image).split('/')[-1].split('.')[0]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def __str__(self):
        return self.name

class Thumbnail(models.Model):
    image_id = models.ForeignKey(OriginalImage, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    height = models.IntegerField()
    image = models.ImageField(upload_to=thumbnail_upload_to, validators=[FileExtensionValidator(allowed_extensions=['jpg','png'])], null=True, blank=True)

    def save(self, *args, **kwargs):
        self.image = make_thumbnail(self.image_id.original_image, self.height)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from account.models import SpecialUser, Plan, ThumbnailSize
from io import BytesIO
from PIL import Image

class TestUploader(APITestCase):
    def setUp(self):
        user_without_plan = User.objects.create_user('user_without_plan', 'strong12345')

        user_with_basic_plan = User.objects.create_user('user_with_basic_plan', 'strong12345')

        user_with_premium_plan = User.objects.create_user('user_with_premium_plan', 'strong12345')

        user_with_enterprice_plan = User.objects.create_user('user_with_enterprice_plan', 'strong12345')

        original = ThumbnailSize(name='original', height='original')
        original.save()
        thumbnail_200_px = ThumbnailSize(name='thumbnail_200_px', height='200')
        thumbnail_200_px.save()
        thumbnail_400_px = ThumbnailSize(name='thumbnail_400_px', height='400')
        thumbnail_400_px.save()

        basic = Plan(name='Basic')
        basic.save()
        basic.thumbnails_id.add(thumbnail_200_px)

        premium = Plan(name='Premium')
        premium.save()
        premium.thumbnails_id.add(original, thumbnail_200_px, thumbnail_400_px)

        enterprice = Plan(name='Enterprice')
        enterprice.save()
        enterprice.thumbnails_id.add(original, thumbnail_200_px, thumbnail_400_px)

        spacial_user_with_basic_plan = SpecialUser(user_id=user_with_basic_plan, plan_id=basic)
        spacial_user_with_basic_plan.save()

        spacial_user_with_premium_plan = SpecialUser(user_id=user_with_premium_plan, plan_id=premium)
        spacial_user_with_premium_plan.save()

        spacial_user_with_enterprice_plan = SpecialUser(user_id=user_with_enterprice_plan, plan_id=enterprice)
        spacial_user_with_enterprice_plan.save()

    def generate_image(self):
        file = BytesIO()
        image = Image.new('RGBA', size=(1000, 1000), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        return file

    def generate_invalid_image(self):
        file = BytesIO()
        image = Image.new('RGBA', size=(1000, 1000), color=(155, 0, 0))
        image.save(file, 'bmp')
        file.name = 'test.bmp'
        file.seek(0)
        return file

    def test_anonymous_user_use_the_api(self):
        response = self.client.get('')
        result = response.json()

        self.assertEqual(response.status_code, 403)
        self.assertIsInstance(result, dict)
        self.assertEqual(result['detail'], 'Authentication credentials were not provided.')

    def test_user_without_plan_use_the_api(self):
        user_without_plan = User.objects.get(username='user_without_plan')
        self.client.force_authenticate(user_without_plan)
        response = self.client.get('')
        result = response.json()

        self.assertEqual(response.status_code, 403)
        self.assertIsInstance(result, dict)
        self.assertEqual(result['detail'], 'You do not have a plan yet.')

    def test_user_with_plan_use_the_api(self):
        user_with_basic_plan = User.objects.get(username='user_with_basic_plan')
        self.client.force_authenticate(user_with_basic_plan)
        response = self.client.get('')
        result = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(result, list)
        self.assertEqual(result, [])

    def test_user_with_basic_plan_upload_image(self):
        user_with_basic_plan = User.objects.get(username='user_with_basic_plan')
        self.client.force_authenticate(user_with_basic_plan)

        image = self.generate_image()

        image_name = image.name.split('.')[0]

        data = {
                'original_image': image
            }

        response = self.client.post('', data, format='multipart')
        result = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertIsInstance(result, dict)
        self.assertEqual(list(result.keys()), [image_name])
        self.assertEqual(list(result[image_name].keys()), ['thumbnail_200_px'])

    def test_user_with_premium_plan_upload_image(self):
        user_with_premium_plan = User.objects.get(username='user_with_premium_plan')
        self.client.force_authenticate(user_with_premium_plan)

        image = self.generate_image()

        image_name = image.name.split('.')[0]

        data = {
                'original_image': image
            }

        response = self.client.post('', data, format='multipart')
        result = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertIsInstance(result, dict)
        self.assertEqual(list(result.keys()), [image_name])
        self.assertEqual(list(result[image_name].keys()), ['original_image', 'thumbnail_200_px', 'thumbnail_400_px'])

    def test_user_with_enterprice_plan_upload_image(self):
        user_with_enterprice_plan = User.objects.get(username='user_with_enterprice_plan')
        self.client.force_authenticate(user_with_enterprice_plan)

        image = self.generate_image()

        image_name = image.name.split('.')[0]

        data = {
                'original_image': image
            }

        response = self.client.post('', data, format='multipart')
        result = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertIsInstance(result, dict)
        self.assertEqual(list(result.keys()), [image_name])
        self.assertEqual(list(result[image_name].keys()), ['original_image', 'thumbnail_200_px', 'thumbnail_400_px'])

    def test_user_with_plan_upload_invalid_image(self):
        user_with_basic_plan = User.objects.get(username='user_with_basic_plan')
        self.client.force_authenticate(user_with_basic_plan)

        image = self.generate_invalid_image()

        data = {
                'original_image': image
            }

        response = self.client.post('', data, format='multipart')
        result = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertIsInstance(result, dict)
        self.assertEqual(result['original_image'], ['File extension “bmp” is not allowed. Allowed extensions are: jpg, png.'])




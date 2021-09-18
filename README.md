## General info
This is an image uploader which also creates thumbnails.
Project uses the system of user plan and thumbnail size which admin can create in the django-admin panel.
I created all the project in 5 days 4 hours every day.
It was my first django-rest-framework project so the most time took me reading the documentation and fixing bugs.

## Setup

```
$ git clone https://github.com/thekrzeslo/image_uploader
$ docker-compose run web bash -c "python manage.py makemigrations && python manage.py migrate && python manage.py createsuperuser"
$ docker-compose up
```

## How to use

1. Go to 127.0.0.1:8000/admin
2. Login into django-admin
3. Create some Thumbnails sizes (if you want original size image in "Height:" label enter "original")
4. Create Plan for users enter plan name and mark thumbnails size which this plan should contain
5. Create Special User by mark your user from list and plan from list
6. Go to 127.0.0.1:8000 and log in to the api browser (only logged and user with plan can use api)
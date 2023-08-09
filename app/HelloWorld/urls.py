from django.urls import path

from HelloWorld.views import get_data


urlpatterns=[
        path('get_data', get_data),
        ]

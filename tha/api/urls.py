from django.urls import path

from .views import api_compute

app_name = 'api'

urlpatterns = [
    path('v1/compute/', api_compute, name='compute'),
]

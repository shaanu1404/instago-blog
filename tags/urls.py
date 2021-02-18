from django.urls import path

from .views import create_new_tag

urlpatterns = [
    path('create/new/', create_new_tag, name="new-tag"),
]
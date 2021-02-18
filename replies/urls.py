from django.urls import path

from . import views

urlpatterns = [
    path('<int:id>/like/', views.like_reply, name="like-reply"),
    path('<int:blog_id>/<int:user_id>/', views.comment, name="comment"),
]
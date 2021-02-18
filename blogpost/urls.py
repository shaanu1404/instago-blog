from django.urls import path
from .views import home_page, blog_details, CreateBlog, EditBlogView, delete_post, like_blog_post
from tags.views import add_tags

urlpatterns = [
    path('', home_page, name="home"),
    path('blog/create/new', CreateBlog.as_view(), name="create-blog"),
    path('blog/<slug:slug>/', blog_details, name="detail"),
    path('blog/<slug:slug>/edit/', EditBlogView.as_view(), name="edit"),
    path('blog/<slug:slug>/delete/', delete_post, name="delete"),
    path('blog/<slug:slug>/addtag/', add_tags, name="add-tag"),
    path('blog/<slug:slug>/like/', like_blog_post, name="like-post"),
]

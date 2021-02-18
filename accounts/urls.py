from django.urls import path

from .views import (
    follow, 
    unfollow, 
    UserDetails, 
    register_user, 
    AccountsLoginView,
    logout_user,
    user_profile_update,
    UsersListView,
    edit_bio
)

urlpatterns = [
    path('follow/', follow, name="follow"),
    path('unfollow/', unfollow, name="unfollow"),
    path('register/', register_user, name="user-register"),
    path('login/', AccountsLoginView.as_view(), name="user-login"),
    path('logout/', logout_user, name="user-logout"),
    path('people/search/', UsersListView.as_view(), name="search-people"),
    path('user-profile/edit', user_profile_update, name="user-profile-edit"),
    path('user-profile/edit/bio', edit_bio, name="edit-bio"),
    path('user-profile/<str:username>/', UserDetails.as_view(), name="user-profile"),
]

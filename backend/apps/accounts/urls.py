from django.urls import path

from .views import LoginView, LogoutView, UserDetailView, UserListCreateView, me


urlpatterns = [
    path("auth/login", LoginView.as_view(), name="login"),
    path("auth/login/", LoginView.as_view(), name="login-slash"),
    path("auth/logout", LogoutView.as_view(), name="logout"),
    path("auth/logout/", LogoutView.as_view(), name="logout-slash"),
    path("me", me, name="me"),
    path("me/", me, name="me-slash"),
    path("users", UserListCreateView.as_view(), name="users"),
    path("users/", UserListCreateView.as_view(), name="users-slash"),
    path("users/<uuid:user_id>", UserDetailView.as_view(), name="user-detail"),
    path("users/<uuid:user_id>/", UserDetailView.as_view(), name="user-detail-slash"),
]

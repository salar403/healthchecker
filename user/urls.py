from django.urls import path
from user import views

urlpatterns = [
    path("auth/login/", views.UserLogin.as_view(), name="user_login"),
    path("auth/logout/", views.UserLogout.as_view(), name="user_logout"),
]

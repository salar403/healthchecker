from django.urls import path
from user import views

urlpatterns = [
    path("auth/login/", views.UserLogin.as_view(), name="user_login"),
    path("auth/logout/", views.UserLogout.as_view(), name="user_logout"),
    path("service/create/", views.AddService.as_view(), name="add_service"),
    path("service/list/", views.ListServices.as_view(), name="list_services"),
    path("service/delete/", views.DeleteService.as_view(), name="delete_service"),
]

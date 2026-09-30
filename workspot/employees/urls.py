from django.urls import path

from . import views

app_name = "employees"

urlpatterns = [
    path("", views.home, name="home"),
    path("employees/", views.employee_list, name="list"),
    path("employees/<int:pk>/", views.employee_detail, name="detail"),
]

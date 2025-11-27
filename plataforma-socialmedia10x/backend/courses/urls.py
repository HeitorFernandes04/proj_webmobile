# courses/urls.py
from django.urls import path
from . import views

app_name = "courses"

urlpatterns = [
    path("", views.home, name="home"),  # se você usar home dentro do app
    path("curso/<slug:slug>/", views.course_detail, name="course_detail"),
    path("modulo/<int:pk>/", views.module_detail, name="module_detail"),
    path("aula/<int:pk>/", views.lesson_detail, name="lesson_detail"),
    path("aula/<int:pk>/toggle/", views.toggle_lesson_completion, name="toggle_lesson_completion"),
]

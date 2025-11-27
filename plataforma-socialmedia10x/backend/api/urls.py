# api/urls.py
from django.urls import path

from .views import (
    CourseListAPIView,
    CourseDetailAPIView,
    ModuleLessonsAPIView,
    ToggleLessonCompletionAPIView,
)

app_name = "api"  # <<< adiciona isso

urlpatterns = [
    path("courses/", CourseListAPIView.as_view(), name="api_courses_list"),
    path("courses/<slug:slug>/", CourseDetailAPIView.as_view(), name="api_course_detail"),
    path("modules/<int:pk>/lessons/", ModuleLessonsAPIView.as_view(), name="api_module_lessons"),
    path(
        "lessons/<int:pk>/toggle-completion/",
        ToggleLessonCompletionAPIView.as_view(),
        name="api_toggle_lesson_completion",
    ),
]

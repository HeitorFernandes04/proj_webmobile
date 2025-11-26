from django.urls import path
from .views import (
    home,
    course_detail,
    module_detail,
    lesson_detail,
    toggle_lesson_completion,
)

app_name = "courses"

urlpatterns = [
    # Home da plataforma (lista de cursos)
    path("", home, name="home_courses"),

    # Detalhe de curso (mostra módulos)
    path("courses/<slug:slug>/", course_detail, name="course_detail"),

    # Detalhe de módulo (mostra aulas)
    path("modules/<int:pk>/", module_detail, name="module_detail"),

    # Detalhe de aula
    path("lessons/<int:pk>/", lesson_detail, name="lesson_detail"),

    # Marcar/desmarcar aula como concluída
    path(
        "lessons/<int:pk>/toggle-complete/",
        toggle_lesson_completion,
        name="toggle_lesson_completion",
    ),
]

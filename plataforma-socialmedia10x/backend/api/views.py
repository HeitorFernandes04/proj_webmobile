# api/views.py
from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from courses.models import Course, Module, Lesson, LessonProgress
from .serializers import CourseSerializer, ModuleSerializer, LessonSerializer
from .permissions import HasActiveSubscription


class CourseListAPIView(generics.ListAPIView):
    """
    GET /api/courses/
    Lista todos os cursos com progresso do usuário.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated, HasActiveSubscription]


class CourseDetailAPIView(generics.RetrieveAPIView):
    """
    GET /api/courses/<slug>/
    Detalhes de um curso + módulos com progresso.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    lookup_field = "slug"
    permission_classes = [permissions.IsAuthenticated, HasActiveSubscription]


class ModuleLessonsAPIView(generics.ListAPIView):
    """
    GET /api/modules/<id>/lessons/
    Lista as aulas de um módulo, indicando se cada uma está concluída.
    """
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated, HasActiveSubscription]

    def get_queryset(self):
        module_id = self.kwargs["pk"]
        module = get_object_or_404(Module, pk=module_id)
        return module.lessons.all()


class ToggleLessonCompletionAPIView(APIView):
    """
    POST /api/lessons/<id>/toggle-completion/
    Alterna o status de conclusão de uma aula para o usuário logado.
    """
    permission_classes = [permissions.IsAuthenticated, HasActiveSubscription]

    def post(self, request, pk):
        lesson = get_object_or_404(Lesson, pk=pk)
        lp, created = LessonProgress.objects.get_or_create(
            user=request.user,
            lesson=lesson,
        )

        lp.completed = not lp.completed
        lp.completed_at = timezone.now() if lp.completed else None
        lp.save()

        return Response(
            {"lesson_id": lesson.id, "completed": lp.completed},
            status=status.HTTP_200_OK,
        )

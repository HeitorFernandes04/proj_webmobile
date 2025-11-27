from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from billing.decorators import subscription_required
from .models import Course, Module, Lesson, LessonProgress


def landing_page(request):
    """
    Página pública de vendas (landing page).
    Aqui o usuário conhece o curso e pode ir para login/cadastro.
    """
    return render(request, "landing.html")


@subscription_required
def home(request):
    """
    Home da plataforma (dashboard):
    - Só acessa quem tiver assinatura ativa (decorator subscription_required)
    - Lista os cursos com o progresso do aluno logado.
    """
    courses = Course.objects.all()

    courses_with_progress = []
    for course in courses:
        progress = course.progress_for_user(request.user)
        courses_with_progress.append(
            {
                "course": course,
                "progress": progress,
            }
        )

    context = {
        "courses_with_progress": courses_with_progress,
    }
    return render(request, "courses/home.html", context)


@login_required
def course_detail(request, slug):
    """
    Página de um curso específico:
    - Mostra informações do curso
    - Lista os módulos com progresso por módulo para o aluno logado.
    """
    course = get_object_or_404(Course, slug=slug)
    modules = course.modules.all()

    modules_with_progress = []
    for module in modules:
        progress = module.progress_for_user(request.user)
        modules_with_progress.append(
            {
                "module": module,
                "progress": progress,
            }
        )

    context = {
        "course": course,
        "modules_with_progress": modules_with_progress,
        "course_progress": course.progress_for_user(request.user),
    }
    return render(request, "courses/course_detail.html", context)


@login_required
def module_detail(request, pk):
    """
    Página de um módulo:
    - Lista as aulas do módulo
    - Mostra o progresso do usuário nesse módulo.
    """
    module = get_object_or_404(Module, pk=pk)
    lessons = module.lessons.all()

    lessons_data = []
    for lesson in lessons:
        lp = LessonProgress.objects.filter(
            user=request.user,
            lesson=lesson,
        ).first()
        completed = lp.completed if lp else False

        lessons_data.append(
            {
                "lesson": lesson,
                "completed": completed,
            }
        )

    progress = module.progress_for_user(request.user)

    context = {
        "module": module,
        "lessons_data": lessons_data,
        "progress": progress,
    }
    return render(request, "courses/module_detail.html", context)


@login_required
def lesson_detail(request, pk):
    """
    Página da aula:
    - Mostra o conteúdo/vídeo da aula
    - Garante que existe um registro de progresso para o usuário
      (LessonProgress), que será usado para marcar como concluída.
    """
    lesson = get_object_or_404(Lesson, pk=pk)
    lp, created = LessonProgress.objects.get_or_create(
        user=request.user,
        lesson=lesson,
        defaults={"completed": False},
    )

    context = {
        "lesson": lesson,
        "progress_obj": lp,
    }
    return render(request, "courses/lesson_detail.html", context)


@login_required
def toggle_lesson_completion(request, pk):
    """
    Alterna o status de conclusão da aula para o aluno logado.
    - Se for GET, só redireciona de volta para a aula
    - Se for POST, inverte completed e atualiza completed_at.
    """
    if request.method != "POST":
        return redirect("courses:lesson_detail", pk=pk)

    lesson = get_object_or_404(Lesson, pk=pk)
    lp, created = LessonProgress.objects.get_or_create(
        user=request.user,
        lesson=lesson,
    )

    lp.completed = not lp.completed
    lp.completed_at = timezone.now() if lp.completed else None
    lp.save()

    return redirect("courses:lesson_detail", pk=pk)

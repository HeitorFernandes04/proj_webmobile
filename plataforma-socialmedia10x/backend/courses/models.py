from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL  # ainda usamos no LessonProgress


class Course(models.Model):
    """
    Representa um curso da plataforma.
    Agora sem campo de instrutor, já que a plataforma é de um único professor.
    """
    title = models.CharField("Título", max_length=200)
    slug = models.SlugField("Slug", unique=True)
    description = models.TextField("Descrição")
    created_at = models.DateTimeField("Criado em", auto_now_add=True)

    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"
        ordering = ["title"]

    def __str__(self):
        return self.title

    def total_lessons(self):
        """Total de aulas do curso (somando todos os módulos)."""
        return Lesson.objects.filter(module__course=self).count()

    def progress_for_user(self, user):
        """Progresso geral do curso para um aluno em % (0–100)."""
        total = self.total_lessons()
        if total == 0:
            return 0
        completed = LessonProgress.objects.filter(
            user=user,
            completed=True,
            lesson__module__course=self
        ).count()
        return int((completed / total) * 100)


class Module(models.Model):
    """
    Módulo dentro de um curso.
    """
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="modules",
        verbose_name="Curso"
    )
    title = models.CharField("Título", max_length=200)
    description = models.TextField("Descrição", blank=True)
    order = models.PositiveIntegerField(
        "Ordem",
        default=0,
        help_text="Ordem em que o módulo aparece dentro do curso."
    )

    class Meta:
        verbose_name = "Módulo"
        verbose_name_plural = "Módulos"
        ordering = ["order"]
        unique_together = ("course", "order")

    def __str__(self):
        return f"{self.course.title} - {self.title}"

    def total_lessons(self):
        return self.lessons.count()

    def progress_for_user(self, user):
        """Progresso do módulo para um aluno em % (0–100)."""
        total = self.total_lessons()
        if total == 0:
            return 0
        completed = LessonProgress.objects.filter(
            user=user,
            completed=True,
            lesson__module=self
        ).count()
        return int((completed / total) * 100)


class Lesson(models.Model):
    """
    Aula dentro de um módulo.
    """
    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name="lessons",
        verbose_name="Módulo"
    )
    title = models.CharField("Título", max_length=200)
    video_url = models.URLField(
        "URL do vídeo",
        blank=True,
        help_text="URL do vídeo (ex: link incorporável do YouTube)."
    )
    content = models.TextField(
        "Conteúdo complementar",
        blank=True,
        help_text="Descrição, anotações ou material complementar da aula."
    )
    order = models.PositiveIntegerField(
        "Ordem",
        default=0,
        help_text="Ordem em que a aula aparece dentro do módulo."
    )

    class Meta:
        verbose_name = "Aula"
        verbose_name_plural = "Aulas"
        ordering = ["order"]
        unique_together = ("module", "order")

    def __str__(self):
        return self.title


class LessonProgress(models.Model):
    """
    Marca se um aluno concluiu ou não uma aula.
    Usado para calcular o progresso de módulos e cursos.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="lesson_progress",
        verbose_name="Aluno"
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="progress",
        verbose_name="Aula"
    )
    completed = models.BooleanField("Concluída", default=False)
    completed_at = models.DateTimeField("Data de conclusão", null=True, blank=True)

    class Meta:
        verbose_name = "Progresso de Aula"
        verbose_name_plural = "Progressos de Aulas"
        unique_together = ("user", "lesson")

    def __str__(self):
        status = "OK" if self.completed else "Pendente"
        return f"{self.user} - {self.lesson} ({status})"

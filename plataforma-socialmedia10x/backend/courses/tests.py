# courses/tests.py
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model

from billing.models import Plan, Subscription
from .models import Course, Module, Lesson, LessonProgress

User = get_user_model()


class LessonProgressTests(TestCase):
    def setUp(self):
        # Usuário + assinatura ativa
        self.user = User.objects.create_user(
            username="aluno2",
            email="aluno2@example.com",
            password="SenhaForte123!",
        )

        self.plan = Plan.objects.create(
            name="Acesso vitalício SocialMedia10x",
            price=897.00,
            is_active=True,
        )

        Subscription.objects.create(
            user=self.user,
            plan=self.plan,
            status="active",
            start_date=timezone.now(),
            end_date=None,
        )

        # Curso / módulo / aula para testar
        self.course = Course.objects.create(
            title="Curso Teste",
            slug="curso-teste",
            description="Descrição do curso de teste",
        )

        self.module = Module.objects.create(
            course=self.course,
            title="Módulo 1",
            order=1,
        )

        self.lesson = Lesson.objects.create(
            module=self.module,
            title="Aula 1",
            order=1,
            video_url="https://www.youtube.com/embed/dQw4w9WgXcQ",
            content="Conteúdo da aula 1",
        )

    def test_toggle_lesson_completion_cria_e_marca_concluida(self):
        """
        Ao enviar POST para toggle_lesson_completion, deve:
        - criar LessonProgress (se não existir)
        - marcar completed=True
        - redirecionar para lesson_detail
        """
        self.client.login(username="aluno2", password="SenhaForte123!")

        url = reverse("courses:toggle_lesson_completion", args=[self.lesson.id])
        response = self.client.post(url)

        # redireciona para a página da aula
        self.assertRedirects(
            response,
            reverse("courses:lesson_detail", args=[self.lesson.id]),
            fetch_redirect_response=False,
        )

        lp = LessonProgress.objects.get(user=self.user, lesson=self.lesson)
        self.assertTrue(lp.completed)
        self.assertIsNotNone(lp.completed_at)

    def test_progress_do_curso_fica_100_quando_aula_concluida(self):
        """
        Se todas as aulas do curso estão concluídas, progress_for_user deve retornar 100.
        """
        LessonProgress.objects.create(
            user=self.user,
            lesson=self.lesson,
            completed=True,
            completed_at=timezone.now(),
        )

        progress = self.course.progress_for_user(self.user)
        self.assertEqual(progress, 100)

    def test_views_basicas_respondem_200_para_usuario_com_assinatura(self):
        """
        Verifica se home, course_detail e module_detail respondem 200 para usuário com assinatura.
        """
        self.client.login(username="aluno2", password="SenhaForte123!")

        # /home/
        resp_home = self.client.get(reverse("home"))
        self.assertEqual(resp_home.status_code, 200)

        # course_detail
        resp_course = self.client.get(
            reverse("courses:course_detail", args=[self.course.slug])
        )
        self.assertEqual(resp_course.status_code, 200)

        # module_detail
        resp_module = self.client.get(
            reverse("courses:module_detail", args=[self.module.id])
        )
        self.assertEqual(resp_module.status_code, 200)

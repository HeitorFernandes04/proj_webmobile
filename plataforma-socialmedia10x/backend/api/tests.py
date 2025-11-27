from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from billing.models import Subscription
from courses.models import Course, Module, Lesson

User = get_user_model()


class ApiBasicTests(TestCase):
    def setUp(self):
        # usuário + assinatura ativa
        self.user = User.objects.create_user(
            username="apiuser",
            email="api@example.com",
            password="senha123",
        )
        Subscription.objects.create(
            user=self.user,
            active=True,
        )

        # curso simples pra API devolver alguma coisa
        self.course = Course.objects.create(
            title="Curso API Teste",
            slug="curso-api-teste",
            description="Curso só para testar a API",
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
        )

    def test_listagem_cursos_requer_autenticacao(self):
        """
        Se não estiver logado, a API de cursos deve negar acesso
        (ou redirecionar, dependendo de como você configurou).
        """
        # Ajuste a URL para o endpoint real da sua API
        response = self.client.get("/api/courses/")
        # Se você usa DRF com IsAuthenticated, normalmente é 401/403
        self.assertIn(response.status_code, [302, 401, 403])

    def test_listagem_cursos_para_usuario_com_assinatura(self):
        """
        Usuário logado + assinatura ativa consegue consumir a API de cursos.
        """
        self.client.force_login(self.user)

        response = self.client.get("/api/courses/")

        self.assertEqual(response.status_code, 200)
        # Se a API retorna JSON com lista de cursos:
        self.assertIsInstance(response.json(), list)
        self.assertGreaterEqual(len(response.json()), 1)

# billing/tests.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Subscription

User = get_user_model()


class SubscriptionRequiredTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="usuario_teste",
            email="teste@example.com",
            password="senha123",
        )

    def test_home_sem_login_redireciona_para_login(self):
        """
        Usuário NÃO autenticado tentando acessar /home/
        → deve ser redirecionado para a página de login,
          com ?next=/home/ para voltar depois de logar.
        """
        response = self.client.get(reverse("home"))

        expected_url = f"{reverse('login')}?next={reverse('home')}"
        self.assertRedirects(response, expected_url)

    def test_usuario_sem_assinatura_redireciona_para_pagamento(self):
        """
        Usuário logado, mas SEM assinatura ativa
        → deve ser redirecionado para a tela de pagamento.
        """
        self.client.force_login(self.user)

        response = self.client.get(reverse("home"))

        self.assertRedirects(response, reverse("billing:payment"))

    def test_usuario_com_assinatura_ativa_acessa_home(self):
        """
        Usuário logado COM assinatura ativa
        → consegue acessar /home/ normalmente.
        """
        self.client.force_login(self.user)

        Subscription.objects.create(
            user=self.user,
            active=True,
        )

        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "courses/home.html")

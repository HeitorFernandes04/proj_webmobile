# accounts/tests.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class SignupFlowTests(TestCase):
    def test_signup_cria_usuario_e_redireciona_para_pagamento(self):
        data = {
            "username": "aluno_teste",
            "email": "aluno@example.com",
            "password1": "SenhaForte123!",
            "password2": "SenhaForte123!",
        }

        response = self.client.post(reverse("signup"), data)

        # Usuário foi criado
        self.assertEqual(User.objects.count(), 1)

        # Está logado na sessão
        self.assertIn("_auth_user_id", self.client.session)

        # Foi redirecionado para a página de pagamento
        self.assertRedirects(
            response,
            reverse("billing:payment"),  # exige app_name="billing" no billing/urls.py
            fetch_redirect_response=False,
        )


class AuthRequiredTests(TestCase):
    def test_home_sem_login_redireciona_para_login(self):
        """
        /home/ deve exigir autenticação (via subscription_required).
        """
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 302)
        # Geralmente redireciona para /accounts/login/?next=/home/
        self.assertIn(reverse("login"), response.url)

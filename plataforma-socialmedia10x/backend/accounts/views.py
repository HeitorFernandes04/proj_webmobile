# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

from .forms import CustomUserCreationForm


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"
    # se quiser depois, dá pra sobrescrever get_success_url pra checar se o usuário já pagou


def logout_view(request):
    """
    Faz o logout manualmente e redireciona para a landing.
    """
    logout(request)
    return redirect("landing")


def signup(request):
    """
    Tela de cadastro.
    Após cadastrar, o usuário já é autenticado e enviado para a página de pagamento.
    """
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # redireciona direto para o fluxo de pagamento (Mercado Pago)
            return redirect("billing:payment")  # <<< ajuste importante
    else:
        form = CustomUserCreationForm()

    return render(request, "accounts/signup.html", {"form": form})


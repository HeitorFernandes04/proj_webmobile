# billing/decorators.py
from functools import wraps

from django.shortcuts import redirect
from django.urls import reverse

from .models import Subscription


def subscription_required(view_func):
    """
    Regras:
    - Usuário NÃO autenticado  -> redireciona para 'login';
    - Usuário logado, SEM assinatura ativa -> redireciona para 'billing:payment';
    - Usuário logado, COM assinatura ativa -> acessa a view normalmente.
    """

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user

        # 1) Não logado -> vai para página de login
        if not user.is_authenticated:
            login_url = reverse("login")  # /accounts/login/
            # mantém o ?next=/home/ pra voltar depois do login
            return redirect(f"{login_url}?next={request.path}")

        # 2) Logado -> verificar se existe assinatura ativa
        has_subscription = Subscription.objects.filter(
            user=user,
            active=True,
        ).exists()

        if not has_subscription:
            # Sem assinatura -> fluxo de pagamento
            return redirect("billing:payment")

        # 3) Tem assinatura ativa -> pode acessar
        return view_func(request, *args, **kwargs)

    return _wrapped_view

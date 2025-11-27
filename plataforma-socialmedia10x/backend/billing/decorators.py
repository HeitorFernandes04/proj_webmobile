# billing/decorators.py
from functools import wraps

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from .models import Subscription

# billing/decorators.py
from functools import wraps

from django.shortcuts import redirect
from .models import Subscription


def subscription_required(view_func):
    """
    Garante que:
    - Se o usuário NÃO estiver logado → vai para a página de cadastro.
    - Se estiver logado mas NÃO tiver assinatura ativa → vai para o pagamento.
    - Se estiver logado e TIVER assinatura ativa → acessa a view normalmente.
    """

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user

        # 1) Se não estiver autenticado, manda para o cadastro
        if not user.is_authenticated:
            # nome da URL da sua view de cadastro:
            return redirect("signup")

        # 2) Se estiver logado, checa se tem assinatura ativa
        has_subscription = Subscription.objects.filter(user=user, active=True).exists()
        if not has_subscription:
            # sem assinatura → vai para o fluxo de pagamento
            return redirect("billing:payment")

        # 3) Tem assinatura ativa → pode acessar
        return view_func(request, *args, **kwargs)

    return _wrapped_view

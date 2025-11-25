from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def payment_view(request):
    """
    Página de pagamento/ativação do plano.
    Aqui vamos simular o pagamento para o trabalho.
    """
    return render(request, "billing/payment.html")

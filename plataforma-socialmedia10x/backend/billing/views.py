# billing/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.conf import settings
from django.http import HttpResponse

import mercadopago

from .models import Plan, Payment, Subscription
from .mp_utils import gerar_link_pagamento


@login_required
def payment_view(request):
    """
    Fluxo de pagamento único:
    - Não existe escolha de plano na tela.
    - Assim que o usuário acessa /payment/, criamos um pagamento para
      o ÚNICO plano ativo e redirecionamos para o checkout do Mercado Pago.

    Essa view é chamada logo após o cadastro do usuário
    (signup -> redirect('payment')).
    """

    # 1) Se o usuário já tem assinatura ativa, não faz sentido pagar de novo
    active_sub = Subscription.objects.filter(user=request.user, active=True).first()
    if active_sub:
        return redirect("home")

    # 2) Busca o único plano ativo (acesso vitalício à plataforma)
    plan = Plan.objects.filter(is_active=True).first()
    if not plan:
        # Caso o professor esqueça de criar o plano no admin
        return HttpResponse(
            "Nenhum plano ativo configurado. Crie um plano no Django Admin.",
            status=500,
        )

    # 3) Cria o registro de pagamento pendente no banco
    payment = Payment.objects.create(
        user=request.user,
        plan=plan,
        amount=plan.price,
        status="pending",
    )

    # 4) Gera a preferência no Mercado Pago e pega o link
    link_pagamento = gerar_link_pagamento(request, payment)

    # 5) Redireciona o usuário direto para o checkout do Mercado Pago
    return redirect(link_pagamento)


@login_required
def payment_success(request):
    """
    URL configurada como back_urls['success'] na preferência do Mercado Pago.

    Aqui:
    - Lemos payment_id, external_reference e status
    - Confirmamos o pagamento na API do Mercado Pago
    - Se 'approved', marcamos Payment como 'paid' e ativamos a Subscription
    """
    payment_id = request.GET.get("payment_id")
    external_reference = request.GET.get("external_reference")
    status = request.GET.get("status")

    # external_reference = ID do nosso Payment
    payment = get_object_or_404(Payment, id=external_reference, user=request.user)

    sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)

    mp_status = status
    if payment_id:
        # Confirma o pagamento direto na API do Mercado Pago
        result = sdk.payment().get(payment_id)
        mp_data = result.get("response", {})
        mp_status = mp_data.get("status", status)  # approved, rejected, pending...

        payment.mp_payment_id = str(payment_id)

    payment.mp_status = mp_status or ""

    if payment.mp_status == "approved":
        # Marca pagamento como pago
        payment.status = "paid"
        payment.paid_at = timezone.now()
        payment.save()

        # Cria ou atualiza assinatura vitalícia do usuário
        Subscription.objects.update_or_create(
            user=request.user,
            defaults={
                "plan": payment.plan,
                "active": True,
            },
        )

        message = "Pagamento aprovado! Seu acesso vitalício à plataforma foi liberado."
    else:
        payment.status = "failed"
        payment.save()
        message = "Pagamento não foi aprovado. Tente novamente."

    return render(request, "billing/payment_result.html", {
        "payment": payment,
        "message": message,
    })


@login_required
def payment_pending(request):
    """
    URL configurada como back_urls['pending'].
    Usada para pagamentos que ainda não foram confirmados (ex: boleto).
    """
    external_reference = request.GET.get("external_reference")
    payment = None

    if external_reference:
        payment = Payment.objects.filter(
            id=external_reference,
            user=request.user
        ).first()

    message = "Seu pagamento está pendente. Assim que for aprovado, seu acesso será liberado."

    return render(request, "billing/payment_result.html", {
        "payment": payment,
        "message": message,
    })


@login_required
def payment_failure(request):
    """
    URL configurada como back_urls['failure'].
    Usada quando o usuário cancela o pagamento ou ocorre alguma falha.
    """
    external_reference = request.GET.get("external_reference")
    status = request.GET.get("status")

    payment = None
    if external_reference:
        payment = Payment.objects.filter(
            id=external_reference,
            user=request.user
        ).first()
        if payment:
            payment.status = "failed"
            payment.mp_status = status or "failed"
            payment.save()

    message = "Pagamento cancelado ou não concluído. Nenhuma cobrança foi feita."

    return render(request, "billing/payment_result.html", {
        "payment": payment,
        "message": message,
    })

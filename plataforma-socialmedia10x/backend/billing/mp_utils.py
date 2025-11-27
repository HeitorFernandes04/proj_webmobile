import mercadopago
from django.conf import settings
from django.urls import reverse


def gerar_link_pagamento(request, payment):
    """
    Cria uma preferência de pagamento no Mercado Pago
    e retorna o link (init_point) para o checkout.
    """
    sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)

    success_url = request.build_absolute_uri(
        reverse("billing:payment_success")
    )
    pending_url = request.build_absolute_uri(
        reverse("billing:payment_pending")
    )
    failure_url = request.build_absolute_uri(
        reverse("billing:payment_failure")
    )

    plan = payment.plan

    preference_data = {
        "items": [
            {
                "id": f"Plan_{plan.id}",
                "title": plan.name,
                "quantity": 1,
                "currency_id": "BRL",
                "unit_price": float(plan.price),
            },
        ],
        "back_urls": {
            "success": success_url,
            "pending": pending_url,
            "failure": failure_url,
        },
        # REMOVIDO: "auto_return": "approved",
        "external_reference": str(payment.id),
    }

    result = sdk.preference().create(preference_data)

    status = result.get("status")
    response = result.get("response", {})

    if status not in (200, 201):
        # aqui você já está vendo o erro detalhado na tela
        raise Exception(f"Erro ao criar preferência no Mercado Pago: {result}")

    init_point = response.get("init_point") or response.get("sandbox_init_point")
    if not init_point:
        raise Exception(f"'init_point' não retornado na resposta do MP: {response}")

    payment.mp_preference_id = response.get("id", "")
    payment.save()

    return init_point

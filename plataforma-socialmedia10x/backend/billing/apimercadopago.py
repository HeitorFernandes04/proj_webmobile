import mercadopago

def gerar_link_pagamento():
    sdk = mercadopago.SDK("APP_USR-5679301453212124-112703-b1bf7e90c8b130136289fa866829bab0-3019382499")

    payment_data = {
        "items": [
            {
                "id": "Curso_SocialMedia10x_Vitalicio",
                "title": "Curso SocialMedia10x - Vitalício",
                "quantity": 1,
                "currency_id": "BRL",   # corrigido
                "unit_price": 897.00,   # corrigido
            },
        ],
        "back_urls": {
            "success": "https://test.com/success",
            "pending": "https://test.com/pending",
            "failure": "https://test.com/failure",
        },
        # quando o pagamento for aprovado, o usuário volta automático para success
        "auto_return": "approved",
    }

    # não precisa de request_options aqui
    result = sdk.preference().create(payment_data)
    payment = result["response"]

    link_iniciar_pagamento = payment["init_point"]
    return link_iniciar_pagamento






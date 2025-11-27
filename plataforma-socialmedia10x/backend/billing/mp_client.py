# billing/mp_client.py

import mercadopago
from django.conf import settings

def get_mp_sdk():
    return mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)

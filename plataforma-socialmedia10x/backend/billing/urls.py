# billing/urls.py
from django.urls import path
from . import views

app_name = "billing"

urlpatterns = [
    path("", views.payment_view, name="payment"),
    path("sucesso/", views.payment_success, name="payment_success"),
    path("pendente/", views.payment_pending, name="payment_pending"),
    path("falha/", views.payment_failure, name="payment_failure"),
]

# api/permissions.py
from rest_framework.permissions import BasePermission
from billing.models import Subscription


class HasActiveSubscription(BasePermission):
    """
    Permite acesso apenas para usuários autenticados com assinatura ativa.
    """

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        return Subscription.objects.filter(user=user, active=True).exists()

# billing/models.py

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Plan(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='subscription')
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT)
    started_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user} - {self.plan} ({'ativa' if self.active else 'inativa'})"


class Payment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pendente'),
        ('paid', 'Pago'),
        ('failed', 'Falhou'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    # campos ligados ao Mercado Pago
    mp_preference_id = models.CharField(
        max_length=100,
        blank=True,
        help_text="ID da preferência criada no Mercado Pago"
    )
    mp_payment_id = models.CharField(
        max_length=100,
        blank=True,
        help_text="ID do pagamento retornado pelo Mercado Pago"
    )
    mp_status = models.CharField(
        max_length=50,
        blank=True,
        help_text="Status bruto retornado pelo Mercado Pago (approved, pending, etc.)"
    )

    def __str__(self):
        return f"Pagamento {self.id} - {self.user} - {self.status}"

    def mark_as_paid(self):
        from django.utils import timezone
        self.status = 'paid'
        self.paid_at = timezone.now()
        self.save()

        # cria/atualiza assinatura
        Subscription.objects.update_or_create(
            user=self.user,
            defaults={'plan': self.plan, 'active': True},
        )

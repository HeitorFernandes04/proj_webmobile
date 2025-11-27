# billing/models.py

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class Plan(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Subscription(models.Model):
    """
    Assinatura do usuário.

    Compatível com:
    - Seu fluxo atual (active + plan opcional)
    - Os testes antigos, que ainda usam: status, start_date, end_date
    """

    STATUS_CHOICES = (
        ("active", "Ativa"),
        ("canceled", "Cancelada"),
        ("expired", "Expirada"),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="subscription",
    )

    # Plano pode ser nulo para permitir:
    # Subscription.objects.create(user=..., active=True, ...)
    plan = models.ForeignKey(
        Plan,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    # Campo que você já tinha
    started_at = models.DateTimeField(auto_now_add=True)

    # Campos que os TESTES esperam
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="active",
    )
    start_date = models.DateTimeField(
        default=timezone.now,
    )
    end_date = models.DateTimeField(
        null=True,
        blank=True,
    )

    # Campo usado pelo decorator e pelo seu fluxo
    active = models.BooleanField(default=True)

    def __str__(self):
        status_label = dict(self.STATUS_CHOICES).get(self.status, self.status)
        return f"{self.user} - {self.plan or 'sem plano'} ({status_label})"

    @property
    def is_active(self):
        """
        Helper pra saber se a assinatura está “ativa de verdade”.
        """
        if not self.active:
            return False
        if self.status != "active":
            return False
        if self.end_date and self.end_date < timezone.now():
            return False
        return True


class Payment(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pendente"),
        ("paid", "Pago"),
        ("failed", "Falhou"),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="payments",
    )
    plan = models.ForeignKey(
        Plan,
        on_delete=models.PROTECT,
    )
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    # campos ligados ao Mercado Pago
    mp_preference_id = models.CharField(
        max_length=100,
        blank=True,
        help_text="ID da preferência criada no Mercado Pago",
    )
    mp_payment_id = models.CharField(
        max_length=100,
        blank=True,
        help_text="ID do pagamento retornado pelo Mercado Pago",
    )
    mp_status = models.CharField(
        max_length=50,
        blank=True,
        help_text="Status bruto retornado pelo Mercado Pago (approved, pending, etc.)",
    )

    def __str__(self):
        return f"Pagamento {self.id} - {self.user} - {self.status}"

    def mark_as_paid(self):
        """
        Marca o pagamento como pago e garante/atualiza a Subscription.
        """
        self.status = "paid"
        self.paid_at = timezone.now()
        self.save()

        # cria/atualiza assinatura
        Subscription.objects.update_or_create(
            user=self.user,
            defaults={
                "plan": self.plan,
                "active": True,
                "status": "active",
                "start_date": timezone.now(),
                "end_date": None,
            },
        )

# backend/billing/admin.py
from django.contrib import admin
from .models import Plan, Subscription, Payment


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("user", "plan", "active", "started_at")
    list_filter = ("active", "plan")
    search_fields = ("user__username", "user__email", "plan__name")


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("user", "plan", "amount", "status", "created_at")
    list_filter = ("status", "plan")
    search_fields = ("user__username", "user__email", "plan__name", "mp_payment_id")

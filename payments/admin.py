from django.contrib import admin
from .models import SubscriptionPlan, PaymentTransaction

@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_tnd', 'duration_days')

@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'plan', 'amount', 'status', 'created_at')
    list_filter = ('status',)

from django.db import models
from django.contrib.auth.models import User

class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price_tnd = models.DecimalField(max_digits=6, decimal_places=3) # بالدينار التونسي TND
    duration_days = models.PositiveIntegerField(default=30)

    def __str__(self):
        return f"{self.name} - {self.price_tnd} TND"

class PaymentTransaction(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'قيد الانتظار'),
        ('SUCCESS', 'تمت بنجاح'),
        ('FAILED', 'فشلت'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=6, decimal_places=3)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Tx: {self.payment_id} - {self.status}"

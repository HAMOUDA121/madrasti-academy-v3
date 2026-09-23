from rest_framework import serializers
from .models import SubscriptionPlan, PaymentTransaction

class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = '__all__'

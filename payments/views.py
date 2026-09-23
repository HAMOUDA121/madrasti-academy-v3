import uuid
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import SubscriptionPlan, PaymentTransaction
from .serializers import SubscriptionPlanSerializer

class SubscriptionPlanViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SubscriptionPlan.objects.all()
    serializer_class = SubscriptionPlanSerializer

@method_decorator(csrf_exempt, name='dispatch')
class CreateFlouciPaymentView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        plan_id = request.data.get('plan_id')
        try:
            plan = SubscriptionPlan.objects.get(id=plan_id)
        except SubscriptionPlan.DoesNotExist:
            return Response({'error': 'خطة الاشتراك غير موجودة'}, status=status.HTTP_404_NOT_FOUND)

        # محاكاة إنشاء المعاملة مع بوابة Flouci API
        payment_id = f"flouci_{uuid.uuid4().hex[:10]}"
        tx = PaymentTransaction.objects.create(
            plan=plan,
            payment_id=payment_id,
            amount=plan.price_tnd,
            status='PENDING'
        )

        return Response({
            'payment_id': payment_id,
            'amount': float(plan.price_tnd),
            'currency': 'TND',
            'plan_name': plan.name,
            'message': 'تم إعداد بوابات الدفع Flouci بنجاح'
        })

@method_decorator(csrf_exempt, name='dispatch')
class VerifyPaymentView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        payment_id = request.data.get('payment_id')
        try:
            tx = PaymentTransaction.objects.get(payment_id=payment_id)
            tx.status = 'SUCCESS'
            tx.save()
            return Response({
                'status': 'SUCCESS',
                'message': f'تم دفع مبلغ {tx.amount} DT بنجاح عبر Flouci! تم تفعيل {tx.plan.name}.',
                'plan_name': tx.plan.name
            })
        except PaymentTransaction.DoesNotExist:
            return Response({'error': 'معاملة غير موجودة'}, status=status.HTTP_404_NOT_FOUND)

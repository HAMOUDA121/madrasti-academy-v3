import os

# 1. ????? ???? ???????
os.makedirs('payments', exist_ok=True)

# 2. ??? ??????? Models
models_py = """from django.db import models
from django.contrib.auth.models import User

class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price_tnd = models.DecimalField(max_digits=6, decimal_places=3) # ???????? ??????? TND
    duration_days = models.PositiveIntegerField(default=30)

    def __str__(self):
        return f"{self.name} - {self.price_tnd} TND"

class PaymentTransaction(models.Model):
    STATUS_CHOICES = [
        ('PENDING', '??? ????????'),
        ('SUCCESS', '??? ?????'),
        ('FAILED', '????'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=6, decimal_places=3)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Tx: {self.payment_id} - {self.status}"
"""
with open('payments/models.py', 'w', encoding='utf-8') as f:
    f.write(models_py)

# 3. ??? ??????? Admin
admin_py = """from django.contrib import admin
from .models import SubscriptionPlan, PaymentTransaction

@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_tnd', 'duration_days')

@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'plan', 'amount', 'status', 'created_at')
    list_filter = ('status',)
"""
with open('payments/admin.py', 'w', encoding='utf-8') as f:
    f.write(admin_py)

# 4. ????? REST API
serializers_py = """from rest_framework import serializers
from .models import SubscriptionPlan, PaymentTransaction

class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = '__all__'
"""
with open('payments/serializers.py', 'w', encoding='utf-8') as f:
    f.write(serializers_py)

views_py = """import uuid
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
            return Response({'error': '??? ???????? ??? ??????'}, status=status.HTTP_404_NOT_FOUND)

        # ?????? ????? ???????? ?? ????? Flouci API
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
            'message': '?? ????? ?????? ????? Flouci ?????'
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
                'message': f'?? ??? ???? {tx.amount} DT ????? ??? Flouci! ?? ????? {tx.plan.name}.',
                'plan_name': tx.plan.name
            })
        except PaymentTransaction.DoesNotExist:
            return Response({'error': '?????? ??? ??????'}, status=status.HTTP_404_NOT_FOUND)
"""
with open('payments/views.py', 'w', encoding='utf-8') as f:
    f.write(views_py)

urls_py = """from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SubscriptionPlanViewSet, CreateFlouciPaymentView, VerifyPaymentView

router = DefaultRouter()
router.register(r'plans', SubscriptionPlanViewSet)

urlpatterns = [
    path('create/', CreateFlouciPaymentView.as_view(), name='create_flouci_payment'),
    path('verify/', VerifyPaymentView.as_view(), name='verify_flouci_payment'),
    path('', include(router.urls)),
]
"""
with open('payments/urls.py', 'w', encoding='utf-8') as f:
    f.write(urls_py)

with open('payments/__init__.py', 'w') as f:
    f.write('')

# 5. ????? settings.py
settings_py = """import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'secret-key-123'
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'gamification',
    'ai_assistant',
    'quizzes',
    'payments',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
"""
with open('config/settings.py', 'w', encoding='utf-8') as f:
    f.write(settings_py)

# 6. ????? config/urls.py
config_urls = """from django.contrib import admin
from django.urls import path, include
from .views import home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/gamification/', include('gamification.urls')),
    path('api/ai/', include('ai_assistant.urls')),
    path('api/quizzes/', include('quizzes.urls')),
    path('api/payments/', include('payments.urls')),
    path('', home_view, name='home'),
]
"""
with open('config/urls.py', 'w', encoding='utf-8') as f:
    f.write(config_urls)

# 7. ????? ??????? ???????? ?????? ??? ????? ?? Flouci
index_html = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>???? ?????? | ?????? ??????? V3</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-900 text-slate-100 min-h-screen font-sans">
    
    <!-- Navbar -->
    <nav class="border-b border-slate-800 bg-slate-950/80 backdrop-blur sticky top-0 z-50 px-6 py-4 flex justify-between items-center">
        <div class="flex items-center gap-3">
            <span class="text-3xl">??</span>
            <div>
                <h1 class="text-lg font-bold bg-gradient-to-r from-blue-400 to-indigo-400 bg-clip-text text-transparent">
                    ?????? ??????? V3
                </h1>
                <p class="text-xs text-slate-400">???????? ????????? ???????? ????</p>
            </div>
        </div>
        <div class="flex items-center gap-4">
            <span id="streak-badge" class="bg-amber-500/10 border border-amber-500/30 text-amber-400 px-3 py-1.5 rounded-xl text-xs font-semibold flex items-center gap-2">
                ?? <span id="streak-count">0</span> ???? ???????
            </span>
            <a href="/admin/" class="bg-indigo-600 hover:bg-indigo-500 text-white px-4 py-2 rounded-xl text-xs font-semibold transition">
                ???? ???????
            </a>
        </div>
    </nav>

    <main class="max-w-7xl mx-auto p-6 md:p-8 space-y-8">
        
        <!-- Student Profile Card -->
        <div class="bg-gradient-to-r from-indigo-950/60 to-slate-900 border border-indigo-500/30 rounded-2xl p-6 md:p-8 shadow-xl">
            <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
                <div class="space-y-2">
                    <div class="inline-block bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 px-3 py-1 rounded-full text-xs font-medium" id="student-grade">
                        ???? ???????...
                    </div>
                    <h2 class="text-2xl md:text-3xl font-bold text-white flex items-center gap-3">
                        <span id="student-name">...</span>
                        <span class="bg-emerald-500/20 text-emerald-400 text-xs px-2.5 py-1 rounded-lg border border-emerald-500/30">???</span>
                    </h2>
                    <p class="text-slate-400 text-sm">????? ?? ????? ?????? Django REST Framework</p>
                </div>

                <div class="flex items-center gap-6 bg-slate-900/80 border border-slate-800 p-4 rounded-xl w-full md:w-auto justify-around">
                    <div class="text-center">
                        <p class="text-xs text-slate-400 mb-1">???????</p>
                        <p id="student-level" class="text-3xl font-extrabold text-indigo-400">1</p>
                    </div>
                    <div class="h-8 w-[1px] bg-slate-800"></div>
                    <div class="text-center">
                        <p class="text-xs text-slate-400 mb-1">????? ??? XP</p>
                        <p id="student-xp" class="text-3xl font-extrabold text-amber-400">0</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Section: Flouci Payment Subscriptions -->
        <div class="bg-slate-800/50 border border-slate-700/80 rounded-2xl p-6 space-y-4 shadow-xl">
            <div class="flex items-center justify-between border-b border-slate-700/60 pb-4">
                <div class="flex items-center gap-3">
                    <span class="text-3xl">??</span>
                    <div>
                        <h3 class="font-bold text-lg text-white">?????????? ?????? ?????? (Flouci ????)</h3>
                        <p class="text-xs text-slate-400">????? ?? ??????? ?????? ??????????? ????????? ????? ????? ???????? ???????.</p>
                    </div>
                </div>
            </div>

            <div id="plans-container" class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <p class="text-sm text-slate-400">???? ????? ??? ????????...</p>
            </div>
        </div>

        <!-- Section: Interactive Quizzes -->
        <div class="bg-slate-800/50 border border-slate-700/80 rounded-2xl p-6 space-y-4 shadow-xl">
            <div class="flex items-center justify-between border-b border-slate-700/60 pb-4">
                <div class="flex items-center gap-3">
                    <span class="text-3xl">??</span>
                    <div>
                        <h3 class="font-bold text-lg text-white">???????? ????????? ?????????</h3>
                        <p class="text-xs text-slate-400">????? ???????? ?? ???????? ??????????? ????? ???? XP ??????!</p>
                    </div>
                </div>
            </div>

            <div id="quiz-container" class="space-y-4">
                <p class="text-sm text-slate-400">???? ????? ??????????...</p>
            </div>
        </div>

        <!-- Section: AI Smart Tutor Chat Box -->
        <div class="bg-slate-800/50 border border-slate-700/80 rounded-2xl p-6 space-y-4 shadow-xl">
            <div class="flex items-center justify-between border-b border-slate-700/60 pb-4">
                <div class="flex items-center gap-3">
                    <span class="text-3xl">??</span>
                    <div>
                        <h3 class="font-bold text-lg text-white">?????? ????? (RAG AI Assistant)</h3>
                        <p class="text-xs text-slate-400">???? ?? ?????????? ???????? ?? ??????? ???????? ????? ??? +10 XP!</p>
                    </div>
                </div>
            </div>

            <div id="chat-box" class="bg-slate-950/70 border border-slate-800 rounded-xl p-4 h-48 overflow-y-auto text-sm space-y-3">
                <div class="bg-slate-800/80 p-3 rounded-lg text-slate-300 max-w-xl">
                    ?? ????? ??! ??? ?????? ???????? ???????. ???? ???? ????? ????? ?????????.
                </div>
            </div>

            <div class="flex gap-3">
                <input type="text" id="ai-question" placeholder="???? ????? ???..." class="flex-grow bg-slate-900 border border-slate-700 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-indigo-500 text-white">
                <button onclick="askAI()" class="bg-indigo-600 hover:bg-indigo-500 text-white px-6 py-3 rounded-xl font-bold text-sm transition shadow-lg shadow-indigo-600/30">
                    ?????
                </button>
            </div>
        </div>

        <!-- Badges Section -->
        <div>
            <h3 class="text-xl font-bold text-white mb-4 flex items-center gap-2">
                <span>??</span> ??????? ???????? ????????
            </h3>
            <div id="badges-container" class="grid grid-cols-1 md:grid-cols-3 gap-4"></div>
        </div>

    </main>

    <script>
        let currentQuizId = null;

        async function loadProfileData() {
            try {
                const resProfiles = await fetch('/api/gamification/profiles/');
                const profiles = await resProfiles.json();
                if (profiles && profiles.length > 0) {
                    const student = profiles[0];
                    document.getElementById('student-name').innerText = student.username;
                    document.getElementById('student-grade').innerText = student.grade_display;
                    document.getElementById('student-level').innerText = student.level;
                    document.getElementById('student-xp').innerText = student.xp_points + ' XP';
                    document.getElementById('streak-count').innerText = student.streak_days;
                }

                const resBadges = await fetch('/api/gamification/badges/');
                const badges = await resBadges.json();
                const container = document.getElementById('badges-container');
                container.innerHTML = '';
                badges.forEach(b => {
                    container.innerHTML += `
                        <div class="bg-slate-800/60 border border-slate-700/60 rounded-xl p-5 flex items-start gap-4">
                            <div class="text-3xl bg-slate-900 p-3 rounded-xl border border-slate-800">${b.icon}</div>
                            <div>
                                <h4 class="font-bold text-white text-base">${b.title}</h4>
                                <p class="text-xs text-slate-400 my-1">${b.description}</p>
                                <span class="inline-block bg-amber-500/10 text-amber-400 text-[10px] px-2 py-0.5 rounded font-semibold border border-amber-500/20">
                                    ?????: ${b.xp_required} XP
                                </span>
                            </div>
                        </div>
                    `;
                });

                loadPlans();
                loadQuizzes();
            } catch (err) {
                console.error(err);
            }
        }

        async function loadPlans() {
            const res = await fetch('/api/payments/plans/');
            const plans = await res.json();
            const container = document.getElementById('plans-container');
            container.innerHTML = '';

            plans.forEach(p => {
                container.innerHTML += `
                    <div class="bg-slate-900/80 p-5 rounded-xl border border-slate-700/80 flex justify-between items-center gap-4">
                        <div>
                            <h4 class="font-bold text-white text-base">${p.name}</h4>
                            <p class="text-xs text-slate-400 my-1">${p.description}</p>
                            <span class="text-emerald-400 font-extrabold text-lg">${p.price_tnd} DT</span>
                        </div>
                        <button onclick="payWithFlouci(${p.id})" class="bg-sky-600 hover:bg-sky-500 text-white px-5 py-2.5 rounded-xl text-xs font-bold transition shadow-lg shadow-sky-600/20 whitespace-nowrap">
                            ???? ??? Flouci ??
                        </button>
                    </div>
                `;
            });
        }

        async function payWithFlouci(planId) {
            const res = await fetch('/api/payments/create/', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({plan_id: planId})
            });
            const data = await res.json();

            // ????? ???????? ???????? ????????
            const verifyRes = await fetch('/api/payments/verify/', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({payment_id: data.payment_id})
            });
            const verifyData = await verifyRes.json();
            alert(`???? Flouci Payment Status:\n${verifyData.message}`);
        }

        async function loadQuizzes() {
            const res = await fetch('/api/quizzes/');
            const quizzes = await res.json();
            const container = document.getElementById('quiz-container');
            if(quizzes.length === 0) {
                container.innerHTML = '<p class="text-xs text-slate-400">?? ???? ???????? ????? ??????.</p>';
                return;
            }

            const q = quizzes[0];
            currentQuizId = q.id;
            let html = `
                <div class="bg-slate-900/80 p-5 rounded-xl border border-slate-700 space-y-4">
                    <div class="flex justify-between items-center border-b border-slate-800 pb-3">
                        <h4 class="font-bold text-indigo-300 text-base">${q.title} (${q.subject})</h4>
                        <span class="bg-amber-500/10 text-amber-400 border border-amber-500/30 text-xs px-3 py-1 rounded-full font-semibold">+${q.xp_reward} XP ??? ???????</span>
                    </div>
                    <form id="quiz-form" class="space-y-4">
            `;

            q.questions.forEach((qItem, idx) => {
                html += `
                    <div class="space-y-2">
                        <p class="text-sm font-semibold text-white">${idx + 1}. ${qItem.text}</p>
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-2">
                `;
                qItem.choices.forEach(c => {
                    html += `
                        <label class="flex items-center gap-2 bg-slate-800/80 p-2.5 rounded-lg border border-slate-700/60 hover:border-indigo-500 cursor-pointer text-xs">
                            <input type="radio" name="q_${qItem.id}" value="${c.id}" class="accent-indigo-500">
                            <span>${c.text}</span>
                        </label>
                    `;
                });
                html += `</div></div>`;
            });

            html += `
                    </form>
                    <div class="flex justify-between items-center pt-2">
                        <button onclick="submitQuiz()" class="bg-emerald-600 hover:bg-emerald-500 text-white px-6 py-2.5 rounded-xl text-xs font-bold transition">
                            ????? ????????
                        </button>
                        <span id="quiz-result" class="text-sm font-bold"></span>
                    </div>
                </div>
            `;
            container.innerHTML = html;
        }

        async function submitQuiz() {
            if(!currentQuizId) return;
            const form = document.getElementById('quiz-form');
            const formData = new FormData(form);
            const answers = {};

            for(let [key, val] of formData.entries()) {
                const qId = key.replace('q_', '');
                answers[qId] = parseInt(val);
            }

            const res = await fetch(`/api/quizzes/submit/${currentQuizId}/`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({answers: answers})
            });

            const data = await res.json();
            const resultSpan = document.getElementById('quiz-result');

            if(data.score_pct >= 50) {
                resultSpan.className = 'text-emerald-400 text-sm font-bold';
                resultSpan.innerText = `?? ?????! ???????: ${data.score_pct}% (${data.correct_count}/${data.total_questions}) - ???? ??? +${data.xp_earned} XP!`;
                document.getElementById('student-xp').innerText = data.new_total_xp + ' XP';
                document.getElementById('student-level').innerText = data.new_level;
            } else {
                resultSpan.className = 'text-amber-400 text-sm font-bold';
                resultSpan.innerText = `???????: ${data.score_pct}% (${data.correct_count}/${data.total_questions}) - ???? ?????? ?????? 50% ?? ???? ??????? ??? ??? XP!`;
            }
        }

        async function askAI() {
            const input = document.getElementById('ai-question');
            const q = input.value.trim();
            if(!q) return;

            const chatBox = document.getElementById('chat-box');
            chatBox.innerHTML += `<div class="bg-indigo-900/50 border border-indigo-500/30 p-3 rounded-lg text-indigo-100 max-w-xl ml-auto text-right">${q}</div>`;
            input.value = '';

            try {
                const res = await fetch('/api/ai/chat/', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({question: q})
                });
                const data = await res.json();
                if (data.answer) {
                    chatBox.innerHTML += `<div class="bg-slate-800/80 p-3 rounded-lg text-slate-200 max-w-xl">?? ${data.answer} <span class="text-amber-400 text-xs block mt-1">+${data.xp_earned} XP ??</span></div>`;
                    document.getElementById('student-xp').innerText = data.new_total_xp + ' XP';
                    document.getElementById('student-level').innerText = data.new_level;
                }
                chatBox.scrollTop = chatBox.scrollHeight;
            } catch (err) {
                chatBox.innerHTML += `<div class="text-red-400 p-2 text-xs">??? ??? ????? ???????.</div>`;
            }
        }

        document.addEventListener('DOMContentLoaded', loadProfileData);
    </script>
</body>
</html>
"""
with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(index_html)

print("?? ???? ????? Flouci ?????? ??????? ?????!")

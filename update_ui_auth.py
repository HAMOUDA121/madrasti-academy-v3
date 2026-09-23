import os

index_html = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>لوحة الطالب | مدرستي أكاديمي V3</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-900 text-slate-100 min-h-screen font-sans">
    
    <!-- Navbar -->
    <nav class="border-b border-slate-800 bg-slate-950/80 backdrop-blur sticky top-0 z-50 px-6 py-4 flex justify-between items-center">
        <div class="flex items-center gap-3">
            <span class="text-3xl">🎓</span>
            <div>
                <h1 class="text-lg font-bold bg-gradient-to-r from-blue-400 to-indigo-400 bg-clip-text text-transparent">
                    مدرستي أكاديمي V3
                </h1>
                <p class="text-xs text-slate-400">المنظومة التعليمية التونسية 🇹🇳</p>
            </div>
        </div>

        <div class="flex items-center gap-3" id="auth-nav">
            <!-- سيتم تحميل حالة الحساب هنا تلقائياً -->
            <button onclick="toggleModal('login-modal')" class="text-slate-300 hover:text-white text-xs font-semibold px-3 py-2">تسجيل الدخول</button>
            <button onclick="toggleModal('register-modal')" class="bg-indigo-600 hover:bg-indigo-500 text-white px-4 py-2 rounded-xl text-xs font-semibold shadow">حساب جديد</button>
        </div>
    </nav>

    <main class="max-w-7xl mx-auto p-6 md:p-8 space-y-8">
        
        <!-- Student Profile Card -->
        <div class="bg-gradient-to-r from-indigo-950/60 to-slate-900 border border-indigo-500/30 rounded-2xl p-6 md:p-8 shadow-xl">
            <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
                <div class="space-y-2">
                    <div class="inline-block bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 px-3 py-1 rounded-full text-xs font-medium" id="student-grade">
                        غير مسجل
                    </div>
                    <h2 class="text-2xl md:text-3xl font-bold text-white flex items-center gap-3">
                        <span id="student-name">زائر</span>
                        <span id="student-status-badge" class="bg-slate-700/50 text-slate-400 text-xs px-2.5 py-1 rounded-lg border border-slate-600">زائر</span>
                    </h2>
                    <p class="text-slate-400 text-sm">سجّل دخولك لحفظ النقاط والأوسمة واشتراكاتك</p>
                </div>

                <div class="flex items-center gap-6 bg-slate-900/80 border border-slate-800 p-4 rounded-xl w-full md:w-auto justify-around">
                    <div class="text-center">
                        <p class="text-xs text-slate-400 mb-1">المستوى</p>
                        <p id="student-level" class="text-3xl font-extrabold text-indigo-400">1</p>
                    </div>
                    <div class="h-8 w-[1px] bg-slate-800"></div>
                    <div class="text-center">
                        <p class="text-xs text-slate-400 mb-1">مجموع الـ XP</p>
                        <p id="student-xp" class="text-3xl font-extrabold text-amber-400">0</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Section: Flouci Payment Subscriptions -->
        <div class="bg-slate-800/50 border border-slate-700/80 rounded-2xl p-6 space-y-4 shadow-xl">
            <div class="flex items-center justify-between border-b border-slate-700/60 pb-4">
                <div class="flex items-center gap-3">
                    <span class="text-3xl">💳</span>
                    <div>
                        <h3 class="font-bold text-lg text-white">الاشتراكات والدفع المحلي (Flouci 🇹🇳)</h3>
                        <p class="text-xs text-slate-400">اشترك في المضمون الكامل للباكالوريا والنوفيام وادفع بأمان بالدينار التونسي.</p>
                    </div>
                </div>
            </div>

            <div id="plans-container" class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <p class="text-sm text-slate-400">جاري تحميل خطط الاشتراك...</p>
            </div>
        </div>

        <!-- Section: Interactive Quizzes -->
        <div class="bg-slate-800/50 border border-slate-700/80 rounded-2xl p-6 space-y-4 shadow-xl">
            <div class="flex items-center justify-between border-b border-slate-700/60 pb-4">
                <div class="flex items-center gap-3">
                    <span class="text-3xl">📝</span>
                    <div>
                        <h3 class="font-bold text-lg text-white">التمارين والكويزات التفاعلية</h3>
                        <p class="text-xs text-slate-400">اختبر معلوماتك في امتحانات الباكالوريا واكسب نقاط XP ممتازة!</p>
                    </div>
                </div>
            </div>

            <div id="quiz-container" class="space-y-4">
                <p class="text-sm text-slate-400">جاري تحميل الاختبارات...</p>
            </div>
        </div>

        <!-- Section: AI Smart Tutor Chat Box -->
        <div class="bg-slate-800/50 border border-slate-700/80 rounded-2xl p-6 space-y-4 shadow-xl">
            <div class="flex items-center justify-between border-b border-slate-700/60 pb-4">
                <div class="flex items-center gap-3">
                    <span class="text-3xl">🤖</span>
                    <div>
                        <h3 class="font-bold text-lg text-white">المعلم الذكي (RAG AI Assistant)</h3>
                        <p class="text-xs text-slate-400">اسأل في الرياضيات، الفيزياء أو المناهج التونسية واحصل على +10 XP!</p>
                    </div>
                </div>
            </div>

            <div id="chat-box" class="bg-slate-950/70 border border-slate-800 rounded-xl p-4 h-48 overflow-y-auto text-sm space-y-3">
                <div class="bg-slate-800/80 p-3 rounded-lg text-slate-300 max-w-xl">
                    👋 أهلاً بك! أنا مساعدك التعليمي التونسي. تفضل بطرح سؤالك للبدء بالمراجعة.
                </div>
            </div>

            <div class="flex gap-3">
                <input type="text" id="ai-question" placeholder="اكتب سؤالك هنا..." class="flex-grow bg-slate-900 border border-slate-700 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-indigo-500 text-white">
                <button onclick="askAI()" class="bg-indigo-600 hover:bg-indigo-500 text-white px-6 py-3 rounded-xl font-bold text-sm transition shadow-lg shadow-indigo-600/30">
                    إرسال
                </button>
            </div>
        </div>

        <!-- Badges Section -->
        <div>
            <h3 class="text-xl font-bold text-white mb-4 flex items-center gap-2">
                <span>🏆</span> الشارات والأوسمة المستحقة
            </h3>
            <div id="badges-container" class="grid grid-cols-1 md:grid-cols-3 gap-4"></div>
        </div>

    </main>

    <!-- Modal Login -->
    <div id="login-modal" class="fixed inset-0 bg-black/70 backdrop-blur-sm hidden flex items-center justify-center p-4 z-50">
        <div class="bg-slate-900 border border-slate-800 p-6 rounded-2xl w-full max-w-md space-y-4">
            <h3 class="text-xl font-bold text-white">تسجيل الدخول</h3>
            <div class="space-y-3">
                <input type="text" id="login-username" placeholder="اسم المستخدم" class="w-full bg-slate-800 border border-slate-700 rounded-xl p-3 text-sm text-white focus:outline-none focus:border-indigo-500">
                <input type="password" id="login-password" placeholder="كلمة السر" class="w-full bg-slate-800 border border-slate-700 rounded-xl p-3 text-sm text-white focus:outline-none focus:border-indigo-500">
            </div>
            <div class="flex justify-end gap-3 pt-2">
                <button onclick="toggleModal('login-modal')" class="px-4 py-2 text-slate-400 text-xs">إلغاء</button>
                <button onclick="loginUser()" class="bg-indigo-600 hover:bg-indigo-500 text-white px-5 py-2 rounded-xl text-xs font-bold">دخول</button>
            </div>
        </div>
    </div>

    <!-- Modal Register -->
    <div id="register-modal" class="fixed inset-0 bg-black/70 backdrop-blur-sm hidden flex items-center justify-center p-4 z-50">
        <div class="bg-slate-900 border border-slate-800 p-6 rounded-2xl w-full max-w-md space-y-4">
            <h3 class="text-xl font-bold text-white">إنشاء حساب جديد</h3>
            <div class="space-y-3">
                <input type="text" id="reg-username" placeholder="اسم المستخدم" class="w-full bg-slate-800 border border-slate-700 rounded-xl p-3 text-sm text-white focus:outline-none focus:border-indigo-500">
                <input type="password" id="reg-password" placeholder="كلمة السر" class="w-full bg-slate-800 border border-slate-700 rounded-xl p-3 text-sm text-white focus:outline-none focus:border-indigo-500">
                <select id="reg-grade" class="w-full bg-slate-800 border border-slate-700 rounded-xl p-3 text-sm text-white focus:outline-none focus:border-indigo-500">
                    <option value="BAC_MATH">باكالوريا رياضيات</option>
                    <option value="BAC_INFO">باكالوريا علوم الإعلامية</option>
                    <option value="BAC_SC">باكالوريا علوم تجريبية</option>
                    <option value="9TH_GRADE">التاسعة أساسي (نوفيام)</option>
                </select>
            </div>
            <div class="flex justify-end gap-3 pt-2">
                <button onclick="toggleModal('register-modal')" class="px-4 py-2 text-slate-400 text-xs">إلغاء</button>
                <button onclick="registerUser()" class="bg-emerald-600 hover:bg-emerald-500 text-white px-5 py-2 rounded-xl text-xs font-bold">تسجيل الحساب</button>
            </div>
        </div>
    </div>

    <script>
        let currentQuizId = null;

        function toggleModal(id) {
            const el = document.getElementById(id);
            el.classList.toggle('hidden');
        }

        async function checkAuth() {
            try {
                const res = await fetch('/api/auth/user/');
                const data = await res.json();
                const nav = document.getElementById('auth-nav');

                if (data.authenticated) {
                    document.getElementById('student-name').innerText = data.username;
                    document.getElementById('student-grade').innerText = data.grade;
                    document.getElementById('student-level').innerText = data.level;
                    document.getElementById('student-xp').innerText = data.xp_points + ' XP';
                    
                    const badge = document.getElementById('student-status-badge');
                    badge.innerText = 'طالب مسجل';
                    badge.className = 'bg-emerald-500/20 text-emerald-400 text-xs px-2.5 py-1 rounded-lg border border-emerald-500/30';

                    nav.innerHTML = `
                        <span class="text-xs text-indigo-300 font-bold">👤 ${data.username}</span>
                        <a href="/admin/" class="bg-slate-800 text-slate-300 px-3 py-1.5 rounded-xl text-xs">لوحة الإدارة</a>
                        <button onclick="logoutUser()" class="bg-red-500/20 text-red-400 border border-red-500/30 px-3 py-1.5 rounded-xl text-xs font-semibold">خروج</button>
                    `;
                } else {
                    nav.innerHTML = `
                        <button onclick="toggleModal('login-modal')" class="text-slate-300 hover:text-white text-xs font-semibold px-3 py-2">تسجيل الدخول</button>
                        <button onclick="toggleModal('register-modal')" class="bg-indigo-600 hover:bg-indigo-500 text-white px-4 py-2 rounded-xl text-xs font-semibold shadow">حساب جديد</button>
                    `;
                }

                loadBadges();
                loadPlans();
                loadQuizzes();
            } catch (err) {
                console.error(err);
            }
        }

        async function loginUser() {
            const username = document.getElementById('login-username').value;
            const password = document.getElementById('login-password').value;
            const res = await fetch('/api/auth/login/', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({username, password})
            });
            const data = await res.json();
            if (res.ok) {
                toggleModal('login-modal');
                checkAuth();
            } else {
                alert(data.error || 'خطأ في تسجيل الدخول');
            }
        }

        async function registerUser() {
            const username = document.getElementById('reg-username').value;
            const password = document.getElementById('reg-password').value;
            const grade = document.getElementById('reg-grade').value;
            const res = await fetch('/api/auth/register/', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({username, password, grade})
            });
            const data = await res.json();
            if (res.ok) {
                toggleModal('register-modal');
                checkAuth();
            } else {
                alert(data.error || 'خطأ في إنشاء الحساب');
            }
        }

        async function logoutUser() {
            await fetch('/api/auth/logout/', {method: 'POST'});
            window.location.reload();
        }

        async function loadBadges() {
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
                                تتطلب: ${b.xp_required} XP
                            </span>
                        </div>
                    </div>
                `;
            });
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
                            ادفع عبر Flouci 💳
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

            const verifyRes = await fetch('/api/payments/verify/', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({payment_id: data.payment_id})
            });
            const verifyData = await verifyRes.json();
            alert(`🇹🇳 Flouci Payment Status:\n${verifyData.message}`);
        }

        async function loadQuizzes() {
            const res = await fetch('/api/quizzes/');
            const quizzes = await res.json();
            const container = document.getElementById('quiz-container');
            if(quizzes.length === 0) {
                container.innerHTML = '<p class="text-xs text-slate-400">لا توجد اختبارات متاحة حالياً.</p>';
                return;
            }

            const q = quizzes[0];
            currentQuizId = q.id;
            let html = `
                <div class="bg-slate-900/80 p-5 rounded-xl border border-slate-700 space-y-4">
                    <div class="flex justify-between items-center border-b border-slate-800 pb-3">
                        <h4 class="font-bold text-indigo-300 text-base">${q.title} (${q.subject})</h4>
                        <span class="bg-amber-500/10 text-amber-400 border border-amber-500/30 text-xs px-3 py-1 rounded-full font-semibold">+${q.xp_reward} XP عند الإنجاز</span>
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
                            تسليم الإجابات
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
                resultSpan.innerText = `🎉 ممتاز! النتيجة: ${data.score_pct}% (${data.correct_count}/${data.total_questions}) - حصلت على +${data.xp_earned} XP!`;
                checkAuth();
            } else {
                resultSpan.className = 'text-amber-400 text-sm font-bold';
                resultSpan.innerText = `النتيجة: ${data.score_pct}% (${data.correct_count}/${data.total_questions}) - حاول مجدداً لتحقيق 50% أو أكثر والحصول على الـ XP!`;
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
                    chatBox.innerHTML += `<div class="bg-slate-800/80 p-3 rounded-lg text-slate-200 max-w-xl">🤖 ${data.answer} <span class="text-amber-400 text-xs block mt-1">+${data.xp_earned} XP 🏆</span></div>`;
                    checkAuth();
                }
                chatBox.scrollTop = chatBox.scrollHeight;
            } catch (err) {
                chatBox.innerHTML += `<div class="text-red-400 p-2 text-xs">حدث خطأ أثناء الاتصال.</div>`;
            }
        }

        document.addEventListener('DOMContentLoaded', checkAuth);
    </script>
</body>
</html>
"""
with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(index_html)

print("تم تحديث الواجهة وتضمين شاشات التسجيل والدخول بنجاح!")

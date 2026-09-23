import os

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

        <div class="flex items-center gap-3" id="auth-nav">
            <button onclick="toggleModal('login-modal')" class="text-slate-300 hover:text-white text-xs font-semibold px-3 py-2">????? ??????</button>
            <button onclick="toggleModal('register-modal')" class="bg-indigo-600 hover:bg-indigo-500 text-white px-4 py-2 rounded-xl text-xs font-semibold shadow">???? ????</button>
        </div>
    </nav>

    <main class="max-w-7xl mx-auto p-6 md:p-8 space-y-8">
        
        <!-- Student Profile Card -->
        <div class="bg-gradient-to-r from-indigo-950/60 to-slate-900 border border-indigo-500/30 rounded-2xl p-6 md:p-8 shadow-xl">
            <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
                <div class="space-y-2">
                    <div class="inline-block bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 px-3 py-1 rounded-full text-xs font-medium" id="student-grade">
                        ??? ????
                    </div>
                    <h2 class="text-2xl md:text-3xl font-bold text-white flex items-center gap-3">
                        <span id="student-name">????</span>
                        <span id="student-status-badge" class="bg-slate-700/50 text-slate-400 text-xs px-2.5 py-1 rounded-lg border border-slate-600">????</span>
                    </h2>
                    <p class="text-slate-400 text-sm">???? ????? ???? ?????? ???????? ??????????</p>
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

        <!-- Section: RAG Documents Store -->
        <div class="bg-slate-800/50 border border-slate-700/80 rounded-2xl p-6 space-y-4 shadow-xl">
            <div class="flex items-center justify-between border-b border-slate-700/60 pb-4">
                <div class="flex items-center gap-3">
                    <span class="text-3xl">??</span>
                    <div>
                        <h3 class="font-bold text-lg text-white">????? ??????? ????????? ??????????? (RAG Store)</h3>
                        <p class="text-xs text-slate-400">??????? ???????? ??? ????? ???? ???????? ???????? ????? ??????? ?????? ?????.</p>
                    </div>
                </div>
                <button onclick="toggleModal('upload-doc-modal')" class="bg-emerald-600 hover:bg-emerald-500 text-white px-4 py-2 rounded-xl text-xs font-bold transition">
                    + ??? ????? PDF
                </button>
            </div>

            <div id="documents-container" class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <p class="text-sm text-slate-400">???? ????? ???????...</p>
            </div>
        </div>

        <!-- Section: AI Smart Tutor Chat Box -->
        <div class="bg-slate-800/50 border border-slate-700/80 rounded-2xl p-6 space-y-4 shadow-xl">
            <div class="flex items-center justify-between border-b border-slate-700/60 pb-4">
                <div class="flex items-center gap-3">
                    <span class="text-3xl">??</span>
                    <div>
                        <h3 class="font-bold text-lg text-white">?????? ????? ??????? ?? RAG (Gemini AI)</h3>
                        <p class="text-xs text-slate-400">???? ?? ?????????? ???????? ?? ??????? ???????? ?????? ?????? ????????? ?? ??????? ????????!</p>
                    </div>
                </div>
            </div>

            <div id="chat-box" class="bg-slate-950/70 border border-slate-800 rounded-xl p-4 h-56 overflow-y-auto text-sm space-y-3">
                <div class="bg-slate-800/80 p-3 rounded-lg text-slate-300 max-w-xl">
                    ?? ????? ??! ??? ????? ????? ??????? ??????? ??????? ????????. ???? ???? ?????.
                </div>
            </div>

            <div class="flex gap-3">
                <input type="text" id="ai-question" placeholder="???? ????? ???..." class="flex-grow bg-slate-900 border border-slate-700 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-indigo-500 text-white">
                <button onclick="askAI()" class="bg-indigo-600 hover:bg-indigo-500 text-white px-6 py-3 rounded-xl font-bold text-sm transition shadow-lg shadow-indigo-600/30">
                    ?????
                </button>
            </div>
        </div>

        <!-- Section: Flouci Payment Subscriptions -->
        <div class="bg-slate-800/50 border border-slate-700/80 rounded-2xl p-6 space-y-4 shadow-xl">
            <div class="flex items-center justify-between border-b border-slate-700/60 pb-4">
                <div class="flex items-center gap-3">
                    <span class="text-3xl">??</span>
                    <div>
                        <h3 class="font-bold text-lg text-white">?????????? ?????? ?????? (Flouci ????)</h3>
                        <p class="text-xs text-slate-400">????? ???????? ??????? ?????? ??? ???????.</p>
                    </div>
                </div>
            </div>
            <div id="plans-container" class="grid grid-cols-1 md:grid-cols-2 gap-4"></div>
        </div>

        <!-- Section: Interactive Quizzes -->
        <div class="bg-slate-800/50 border border-slate-700/80 rounded-2xl p-6 space-y-4 shadow-xl">
            <div class="flex items-center justify-between border-b border-slate-700/60 pb-4">
                <div class="flex items-center gap-3">
                    <span class="text-3xl">??</span>
                    <div>
                        <h3 class="font-bold text-lg text-white">???????? ????????? ?????????</h3>
                        <p class="text-xs text-slate-400">????? ???????? ????? XP!</p>
                    </div>
                </div>
            </div>
            <div id="quiz-container" class="space-y-4"></div>
        </div>

    </main>

    <!-- Modal Upload PDF -->
    <div id="upload-doc-modal" class="fixed inset-0 bg-black/70 backdrop-blur-sm hidden flex items-center justify-center p-4 z-50">
        <div class="bg-slate-900 border border-slate-800 p-6 rounded-2xl w-full max-w-md space-y-4">
            <h3 class="text-xl font-bold text-white">??? ???????? / ??? PDF ???????</h3>
            <div class="space-y-3">
                <input type="text" id="doc-title" placeholder="????? ??????? (????: ??? ??????? ??? 2024)" class="w-full bg-slate-800 border border-slate-700 rounded-xl p-3 text-sm text-white focus:outline-none focus:border-indigo-500">
                <input type="text" id="doc-subject" placeholder="?????? (????: ???????)" class="w-full bg-slate-800 border border-slate-700 rounded-xl p-3 text-sm text-white focus:outline-none focus:border-indigo-500">
                <select id="doc-grade" class="w-full bg-slate-800 border border-slate-700 rounded-xl p-3 text-sm text-white focus:outline-none focus:border-indigo-500">
                    <option value="BAC_MATH">????????? ???????</option>
                    <option value="BAC_INFO">????????? ???? ?????????</option>
                    <option value="BAC_SC">????????? ???? ???????</option>
                    <option value="9TH_GRADE">??????? ????? (??????)</option>
                </select>
                <input type="file" id="doc-file" accept=".pdf" class="w-full text-xs text-slate-400 file:mr-4 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-xs file:font-semibold file:bg-indigo-600 file:text-white hover:file:bg-indigo-500">
            </div>
            <div class="flex justify-end gap-3 pt-2">
                <button onclick="toggleModal('upload-doc-modal')" class="px-4 py-2 text-slate-400 text-xs">?????</button>
                <button onclick="uploadDocument()" class="bg-emerald-600 hover:bg-emerald-500 text-white px-5 py-2 rounded-xl text-xs font-bold">??? ??????? RAG</button>
            </div>
        </div>
    </div>

    <!-- Modals Auth -->
    <div id="login-modal" class="fixed inset-0 bg-black/70 backdrop-blur-sm hidden flex items-center justify-center p-4 z-50">
        <div class="bg-slate-900 border border-slate-800 p-6 rounded-2xl w-full max-w-md space-y-4">
            <h3 class="text-xl font-bold text-white">????? ??????</h3>
            <div class="space-y-3">
                <input type="text" id="login-username" placeholder="??? ????????" class="w-full bg-slate-800 border border-slate-700 rounded-xl p-3 text-sm text-white focus:outline-none focus:border-indigo-500">
                <input type="password" id="login-password" placeholder="???? ????" class="w-full bg-slate-800 border border-slate-700 rounded-xl p-3 text-sm text-white focus:outline-none focus:border-indigo-500">
            </div>
            <div class="flex justify-end gap-3 pt-2">
                <button onclick="toggleModal('login-modal')" class="px-4 py-2 text-slate-400 text-xs">?????</button>
                <button onclick="loginUser()" class="bg-indigo-600 hover:bg-indigo-500 text-white px-5 py-2 rounded-xl text-xs font-bold">????</button>
            </div>
        </div>
    </div>

    <div id="register-modal" class="fixed inset-0 bg-black/70 backdrop-blur-sm hidden flex items-center justify-center p-4 z-50">
        <div class="bg-slate-900 border border-slate-800 p-6 rounded-2xl w-full max-w-md space-y-4">
            <h3 class="text-xl font-bold text-white">????? ???? ????</h3>
            <div class="space-y-3">
                <input type="text" id="reg-username" placeholder="??? ????????" class="w-full bg-slate-800 border border-slate-700 rounded-xl p-3 text-sm text-white focus:outline-none focus:border-indigo-500">
                <input type="password" id="reg-password" placeholder="???? ????" class="w-full bg-slate-800 border border-slate-700 rounded-xl p-3 text-sm text-white focus:outline-none focus:border-indigo-500">
                <select id="reg-grade" class="w-full bg-slate-800 border border-slate-700 rounded-xl p-3 text-sm text-white focus:outline-none focus:border-indigo-500">
                    <option value="BAC_MATH">????????? ???????</option>
                    <option value="BAC_INFO">????????? ???? ?????????</option>
                    <option value="BAC_SC">????????? ???? ???????</option>
                    <option value="9TH_GRADE">??????? ????? (??????)</option>
                </select>
            </div>
            <div class="flex justify-end gap-3 pt-2">
                <button onclick="toggleModal('register-modal')" class="px-4 py-2 text-slate-400 text-xs">?????</button>
                <button onclick="registerUser()" class="bg-emerald-600 hover:bg-emerald-500 text-white px-5 py-2 rounded-xl text-xs font-bold">????? ??????</button>
            </div>
        </div>
    </div>

    <script>
        let currentQuizId = null;

        function toggleModal(id) {
            document.getElementById(id).classList.toggle('hidden');
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
                    badge.innerText = '???? ????';
                    badge.className = 'bg-emerald-500/20 text-emerald-400 text-xs px-2.5 py-1 rounded-lg border border-emerald-500/30';

                    nav.innerHTML = `
                        <span class="text-xs text-indigo-300 font-bold">?? ${data.username}</span>
                        <a href="/admin/" class="bg-slate-800 text-slate-300 px-3 py-1.5 rounded-xl text-xs">???? ???????</a>
                        <button onclick="logoutUser()" class="bg-red-500/20 text-red-400 border border-red-500/30 px-3 py-1.5 rounded-xl text-xs font-semibold">????</button>
                    `;
                }

                loadDocuments();
                loadPlans();
                loadQuizzes();
            } catch (err) { console.error(err); }
        }

        async function loadDocuments() {
            const res = await fetch('/api/documents/list/');
            const docs = await res.json();
            const container = document.getElementById('documents-container');
            container.innerHTML = '';

            if (docs.length === 0) {
                container.innerHTML = '<p class="text-xs text-slate-400 col-span-3">?? ???? ????? ?????? ???. ???? ??? "+ ??? ????? PDF" ?????? ???????? ?????? ?????.</p>';
                return;
            }

            docs.forEach(d => {
                container.innerHTML += `
                    <div class="bg-slate-900/80 p-4 rounded-xl border border-slate-700 flex justify-between items-center">
                        <div>
                            <h4 class="font-bold text-white text-sm">${d.title}</h4>
                            <p class="text-xs text-indigo-300">${d.subject} • ${d.grade_display}</p>
                        </div>
                        <a href="${d.file}" target="_blank" class="bg-slate-800 hover:bg-slate-700 text-slate-200 px-3 py-1.5 rounded-lg text-xs font-semibold">
                            ??? ??
                        </a>
                    </div>
                `;
            });
        }

        async function uploadDocument() {
            const title = document.getElementById('doc-title').value;
            const subject = document.getElementById('doc-subject').value;
            const grade = document.getElementById('doc-grade').value;
            const fileInput = document.getElementById('doc-file');

            if (!title || !fileInput.files[0]) {
                alert('???? ????? ??????? ??????? ??? PDF');
                return;
            }

            const formData = new FormData();
            formData.append('title', title);
            formData.append('subject', subject);
            formData.append('grade', grade);
            formData.append('file', fileInput.files[0]);

            const res = await fetch('/api/documents/upload/', {
                method: 'POST',
                body: formData
            });

            const data = await res.json();
            if (res.ok) {
                alert(data.message);
                toggleModal('upload-doc-modal');
                loadDocuments();
            } else {
                alert(data.error || '??? ????? ??? ???????');
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
            if (res.ok) { toggleModal('login-modal'); checkAuth(); } else { alert('??? ?? ????? ??????'); }
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
            if (res.ok) { toggleModal('register-modal'); checkAuth(); } else { alert('??? ?? ???????'); }
        }

        async function logoutUser() {
            await fetch('/api/auth/logout/', {method: 'POST'});
            window.location.reload();
        }

        async function loadPlans() {
            const res = await fetch('/api/payments/plans/');
            const plans = await res.json();
            const container = document.getElementById('plans-container');
            container.innerHTML = '';
            plans.forEach(p => {
                container.innerHTML += `
                    <div class="bg-slate-900/80 p-5 rounded-xl border border-slate-700 flex justify-between items-center">
                        <div>
                            <h4 class="font-bold text-white text-base">${p.name}</h4>
                            <p class="text-xs text-slate-400 my-1">${p.description}</p>
                            <span class="text-emerald-400 font-extrabold text-lg">${p.price_tnd} DT</span>
                        </div>
                        <button onclick="payWithFlouci(${p.id})" class="bg-sky-600 hover:bg-sky-500 text-white px-5 py-2.5 rounded-xl text-xs font-bold transition shadow-lg shadow-sky-600/20">
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
            const verifyRes = await fetch('/api/payments/verify/', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({payment_id: data.payment_id})
            });
            const verifyData = await verifyRes.json();
            alert(`???? Flouci Status:\n${verifyData.message}`);
        }

        async function loadQuizzes() {
            const res = await fetch('/api/quizzes/');
            const quizzes = await res.json();
            const container = document.getElementById('quiz-container');
            if(quizzes.length === 0) return;
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
                answers[key.replace('q_', '')] = parseInt(val);
            }
            const res = await fetch(`/api/quizzes/submit/${currentQuizId}/`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({answers})
            });
            const data = await res.json();
            const resultSpan = document.getElementById('quiz-result');
            if(data.score_pct >= 50) {
                resultSpan.className = 'text-emerald-400 text-sm font-bold';
                resultSpan.innerText = `?? ?????! ???????: ${data.score_pct}% - ???? ??? +${data.xp_earned} XP!`;
                checkAuth();
            } else {
                resultSpan.className = 'text-amber-400 text-sm font-bold';
                resultSpan.innerText = `???????: ${data.score_pct}% - ???? ?????? ?????? 50% ?? ????!`;
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
                    checkAuth();
                }
                chatBox.scrollTop = chatBox.scrollHeight;
            } catch (err) {
                chatBox.innerHTML += `<div class="text-red-400 p-2 text-xs">??? ??? ????? ???????.</div>`;
            }
        }

        document.addEventListener('DOMContentLoaded', checkAuth);
    </script>
</body>
</html>
"""
with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(index_html)

print("?? ????? ??????? ????? ????? RAG Document Store!")

import os

# 1. ????? ????? Dashboard ???????? ????? ?? ??? API ??????
index_html = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>???? ?????? | ?????? ??????? V3</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
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
        
        <!-- Student Profile Card (Dynamic API Data) -->
        <div id="profile-card" class="bg-gradient-to-r from-indigo-950/60 to-slate-900 border border-indigo-500/30 rounded-2xl p-6 md:p-8 shadow-xl relative overflow-hidden">
            <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-6 relative z-10">
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

                <!-- XP & Level Stats -->
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

        <!-- Section: Badges & Rewards -->
        <div>
            <h3 class="text-xl font-bold text-white mb-4 flex items-center gap-2">
                <span>??</span> ??????? ???????? ????????
            </h3>
            <div id="badges-container" class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <!-- Dynamic Content Loaded via JS -->
            </div>
        </div>

        <!-- Section: AI Smart Tutor Quick Access -->
        <div class="bg-slate-800/40 border border-slate-700/60 rounded-2xl p-6 flex flex-col md:flex-row items-center justify-between gap-6">
            <div class="flex items-center gap-4">
                <div class="w-14 h-14 bg-indigo-600/20 border border-indigo-500/40 rounded-2xl flex items-center justify-center text-3xl">
                    ??
                </div>
                <div>
                    <h4 class="font-bold text-lg text-white">?????? ????? (RAG AI Assistant)</h4>
                    <p class="text-xs text-slate-400">?????? ??????? ????????? ??????????? ????????? ??? ???????? ????????.</p>
                </div>
            </div>
            <a href="/api/gamification/" class="bg-indigo-600 hover:bg-indigo-500 text-white px-6 py-3 rounded-xl font-medium text-sm transition shadow-lg shadow-indigo-600/20 whitespace-nowrap">
                ??????? APIs ????????
            </a>
        </div>

    </main>

    <!-- JavaScript to Fetch API Data -->
    <script>
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
                        <div class="bg-slate-800/60 border border-slate-700/60 rounded-xl p-5 flex items-start gap-4 hover:border-indigo-500/50 transition">
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
            } catch (err) {
                console.error("??? ?? ??? ?????? ??? API:", err);
            }
        }

        document.addEventListener('DOMContentLoaded', loadProfileData);
    </script>
</body>
</html>
"""

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(index_html)

print("?? ????? ??????? ???????? ?????? ????? ?? ??? API!")

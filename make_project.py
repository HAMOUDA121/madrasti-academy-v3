import os

files = {
    'requirements.txt': "Django>=4.2,<5.0\ndjangorestframework>=3.14.0\ndjango-cors-headers>=4.3.0\ndjango-environ>=0.11.2\nPillow>=10.1.0\nrequests>=2.31.0\n",
    'manage.py': "#!/usr/bin/env python\nimport os, sys\ndef main():\n    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')\n    from django.core.management import execute_from_command_line\n    execute_from_command_line(sys.argv)\nif __name__ == '__main__':\n    main()\n",
    'config/__init__.py': "",
    'config/urls.py': "from django.contrib import admin\nfrom django.urls import path\nurlpatterns = [path('admin/', admin.site.urls)]\n",
    'config/settings.py': "import os\nfrom pathlib import Path\nBASE_DIR = Path(__file__).resolve().parent.parent\nSECRET_KEY = 'secret-key-123'\nDEBUG = True\nALLOWED_HOSTS = ['*']\nINSTALLED_APPS = ['django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions', 'django.contrib.messages', 'django.contrib.staticfiles', 'rest_framework']\nMIDDLEWARE = ['django.middleware.security.SecurityMiddleware', 'django.contrib.sessions.middleware.SessionMiddleware', 'django.middleware.common.CommonMiddleware', 'django.middleware.csrf.CsrfViewMiddleware', 'django.contrib.auth.middleware.AuthenticationMiddleware', 'django.contrib.messages.middleware.MessageMiddleware']\nROOT_URLCONF = 'config.urls'\nDATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': BASE_DIR / 'db.sqlite3'}}\nSTATIC_URL = 'static/'\nDEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'\n"
}

for path, content in files.items():
    if os.path.dirname(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

print("?? ????? ????? ??????? ?????!")

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

try:
    user = User.objects.filter(username='admin').first()
    if not user:
        user = User.objects.create_superuser('admin', 'tarchihamouda48@gmail.com', 'Admin123456!')
        print('==> SUCCESS: Admin created.')
    else:
        user.set_password('Admin123456!')
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()
        print('==> SUCCESS: Admin updated.')
except Exception as e:
    print(f'==> WARNING: Could not set admin user: {e}')
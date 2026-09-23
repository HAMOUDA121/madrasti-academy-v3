import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

username = os.environ.get('ADMIN_USERNAME', 'admin')
email = os.environ.get('ADMIN_EMAIL', 'tarchihamouda48@gmail.com')
password = os.environ.get('ADMIN_PASSWORD', 'Admin123456!')

user, created = User.objects.get_or_create(username=username, defaults={'email': email})
user.set_password(password)
user.is_staff = True
user.is_superuser = True
user.is_active = True
user.save()

if created:
    print(f"==> Superuser '{username}' created successfully!")
else:
    print(f"==> Superuser '{username}' password and staff permissions updated successfully!")

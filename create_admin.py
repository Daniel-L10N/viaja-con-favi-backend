import os
import sys

sys.path.insert(0, '/home/cmx/viaja-con-favi-backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'viajaconfavi.settings')

import django
django.setup()

from usuarios.models import Usuario

# Create superuser if not exists
if not Usuario.objects.filter(username='admin').exists():
    Usuario.objects.create_superuser(
        username='admin',
        email='viajaconfavi@gmail.com',
        password='Favi2024Admin!'
    )
    print('Superuser created: admin / Favi2024Admin!')
else:
    print('Superuser already exists')
    
# Update password
user = Usuario.objects.get(username='admin')
user.set_password('Favi2024Admin!')
user.save()
print('Password updated')

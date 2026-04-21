import os
import django

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Explicitly set the database URL to point to Render Production DB
os.environ['DATABASE_URL'] = 'postgresql://web_db_zbgs_user:j1zzD9pOkPgz8SzwVi7QHBTc3NIcdsba@dpg-d7jglt8sfn5c73blvsqg-a.frankfurt-postgres.render.com:5432/web_db_zbgs'

# We don't care about Cloudinary or SECRET_KEY just for DB scripts, but we might need dummy values
os.environ.setdefault('SECRET_KEY', 'dummy_key_for_script')

# Disable SSL requirement for local connection to Render DB (as sometimes it causes issues without ssl_require flag in psycopg2)
# Wait, Render requires SSL for external connections, dj-database-url handles it if we append ?sslmode=require
os.environ['DATABASE_URL'] += '?sslmode=require'

django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

username = 'admin'
password = 'admin_password123'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email='admin@example.com', password=password)
    print(f"Superuser created successfully! Username: {username}, Password: {password}")
else:
    u = User.objects.get(username=username)
    u.set_password(password)
    u.save()
    print(f"Superuser already exists. Password reset to: {password}")

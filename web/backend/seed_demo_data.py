import os
import django
from django.contrib.gis.geos import Point

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from directories.models import District, Category
from objects.models import AccessibilityObject, EntranceGroup, SanitaryRooms, ObjectAccessibilityResult
from interactions.models import ForumTopic, ForumPost
from django.contrib.auth import get_user_model

User = get_user_model()

def get_or_create_admin():
    admin = User.objects.filter(is_superuser=True).first()
    if not admin:
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin_password123'
        )
    return admin

def seed():
    print("Starting seeding demo data...")
    
    # 1. Districts
    districts_data = [
        ("Медеуский район", "Медеу ауданы"),
        ("Бостандыкский район", "Бостандық ауданы"),
        ("Алмалинский район", "Алмалы ауданы"),
        ("Ауэзовский район", "Әуезов ауданы"),
        ("Жетысуский район", "Жетісу ауданы"),
        ("Турксибский район", "Түрксіб ауданы"),
        ("Наурызбайский район", "Наурызбай ауданы"),
        ("Алатауский район", "Алатау ауданы"),
    ]
    
    dist_objs = {}
    for ru, kz in districts_data:
        obj, created = District.objects.get_or_create(name_ru=ru, defaults={'name_kz': kz})
        dist_objs[ru] = obj
    
    print(f"Created/found {len(dist_objs)} districts.")

    # 2. Categories
    categories_data = [
        ("Государственные услуги", "Мемлекеттік қызметтер", "#F44336"),
        ("Здравоохранение", "Денсаулық сақтау", "#E91E63"),
        ("Образование", "Білім беру", "#9C27B0"),
        ("Торговля и услуги", "Сауда және қызметтер", "#673AB7"),
        ("Транспорт", "Көлік", "#3F51B5"),
        ("Культура и отдых", "Мәдениет және демалыс", "#2196F3"),
    ]
    
    cat_objs = {}
    for i, (ru, kz, color) in enumerate(categories_data):
        obj, created = Category.objects.get_or_create(name_ru=ru, defaults={'name_kz': kz, 'color': color, 'sort_order': i})
        cat_objs[ru] = obj
    
    print(f"Created/found {len(cat_objs)} categories.")

    # 3. Objects
    # Admin
    admin_user = get_or_create_admin()

    objects_data = [
        {
            "name_ru": "Акимат города Алматы",
            "district": "Медеуский район",
            "category": "Государственные услуги",
            "lat": 43.2382, "lng": 76.9455,
            "access": {"ramp": True, "toilet": True}
        },
        {
            "name_ru": "ЦОН Медеуского района",
            "district": "Медеуский район",
            "category": "Государственные услуги",
            "lat": 43.2505, "lng": 76.9555,
            "access": {"ramp": True, "toilet": False}
        },
        {
            "name_ru": "Центральная аптека №2",
            "district": "Алмалинский район",
            "category": "Здравоохранение",
            "lat": 43.2565, "lng": 76.9425,
            "access": {"ramp": True, "toilet": False}
        },
        {
            "name_ru": "КБТУ (Казахстанско-Британский технический университет)",
            "district": "Алмалинский район",
            "category": "Образование",
            "lat": 43.2551, "lng": 76.9416,
            "access": {"ramp": False, "toilet": False}
        },
        {
            "name_ru": "ТРЦ Mega Center Alma-Ata",
            "district": "Бостандыкский район",
            "category": "Торговля и услуги",
            "lat": 43.2015, "lng": 76.8915,
            "access": {"ramp": True, "toilet": True}
        },
        {
            "name_ru": "Городская поликлиника №4",
            "district": "Бостандыкский район",
            "category": "Здравоохранение",
            "lat": 43.2255, "lng": 76.9085,
            "access": {"ramp": True, "toilet": True}
        },
        {
            "name_ru": "Железнодорожный вокзал Алматы-2",
            "district": "Жетысуский район",
            "category": "Транспорт",
            "lat": 43.2735, "lng": 76.9395,
            "access": {"ramp": True, "toilet": True}
        }
    ]

    for item in objects_data:
        obj, created = AccessibilityObject.objects.get_or_create(
            name_ru=item['name_ru'],
            defaults={
                'district': dist_objs[item['district']],
                'category': cat_objs[item['category']],
                'location': Point(item['lng'], item['lat']),
                'moderation_state': 'approved',
                'created_by': admin_user
            }
        )
        
        # Add access details
        EntranceGroup.objects.get_or_create(object=obj, defaults={'has_ramp': item['access']['ramp']})
        SanitaryRooms.objects.get_or_create(object=obj, defaults={'toilet_accessible': item['access']['toilet']})
        
        # Add summary results (mocked)
        for section in ['Входная группа', 'Пути движения', 'Санитарно-бытовые помещения']:
            status = 'full_accessible' if item['access']['ramp'] and item['access']['toilet'] else 'partial_accessible'
            ObjectAccessibilityResult.objects.get_or_create(
                object=obj, section=section,
                defaults={'k_status': status, 'o_status': status, 'z_status': status, 's_status': status}
            )

    print(f"Seeded {len(objects_data)} accessibility objects.")

    # 4. Forum
    if admin_user:
        topics = [
            "Обсуждение доступности ЦОНов в Алматы",
            "Где найти лучшие пандусы в Медеуском районе?",
            "Вопрос по индукционным петлям в метро"
        ]
        for t_title in topics:
            topic, created = ForumTopic.objects.get_or_create(
                title=t_title,
                defaults={'author': admin_user}
            )
            if created:
                ForumPost.objects.create(
                    topic=topic,
                    author=admin_user,
                    text=f"Всем привет! Давайте обсудим тему: {t_title}. Какие ваши наблюдения?"
                )
    
    print("Seeding forum topics done.")
    print("Demo data seeding completed successfully!")

if __name__ == "__main__":
    try:
        from django.db import connection
        connection.ensure_connection()
        print("Database connection OK")
        seed()
    except Exception as e:
        print(f"SEEDING ERROR: {e}")
        import traceback
        traceback.print_exc()
        # Still exit with 0 if we want the server to start anyway
        # but for debugging we might want to see the error.
        # However, || true in dockerCommand handles exit codes.


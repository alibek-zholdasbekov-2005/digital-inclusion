from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0009_alter_accessibilityobject_options_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='accessibilityobject',
            name='moderation_state',
            field=models.CharField(
                choices=[
                    ('draft', 'Черновик'),
                    ('pending', 'На модерации'),
                    ('approved', 'Одобрено'),
                    ('rejected', 'Отклонено'),
                ],
                default='draft',
                max_length=16,
                verbose_name='Статус модерации',
            ),
        ),
        migrations.AddField(
            model_name='accessibilityobject',
            name='rejection_reason',
            field=models.TextField(blank=True, default='', verbose_name='Причина отклонения'),
        ),
        migrations.AddField(
            model_name='accessibilityobject',
            name='created_by',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=models.SET_NULL,
                related_name='submitted_objects',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name='accessibilityobject',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='accessibilityobject',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='historicalaccessibilityobject',
            name='moderation_state',
            field=models.CharField(
                choices=[
                    ('draft', 'Черновик'),
                    ('pending', 'На модерации'),
                    ('approved', 'Одобрено'),
                    ('rejected', 'Отклонено'),
                ],
                default='draft',
                max_length=16,
                verbose_name='Статус модерации',
            ),
        ),
        migrations.AddField(
            model_name='historicalaccessibilityobject',
            name='rejection_reason',
            field=models.TextField(blank=True, default='', verbose_name='Причина отклонения'),
        ),
        migrations.AddField(
            model_name='historicalaccessibilityobject',
            name='created_by',
            field=models.ForeignKey(
                blank=True, null=True,
                db_constraint=False,
                on_delete=models.DO_NOTHING,
                related_name='+',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name='historicalaccessibilityobject',
            name='created_at',
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
        migrations.AddField(
            model_name='historicalaccessibilityobject',
            name='updated_at',
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
    ]

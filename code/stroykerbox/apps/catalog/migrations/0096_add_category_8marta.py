# -*- coding: utf-8 -*-
"""
Создать категорию «Коллекция 8 марта» (slug 8-marta), если её ещё нет.
Нужна для страницы /catalog/8-marta/ и блока «Сборные букеты» на /8march_design/.
"""
from django.db import migrations


def create_category_8marta(apps, schema_editor):
    # Используем реальную модель, чтобы MPTT проставил lft, rght, level, tree_id при save()
    from stroykerbox.apps.catalog.models import Category
    if not Category.objects.filter(slug='8-marta').exists():
        Category.objects.create(
            name='Коллекция 8 марта',
            slug='8-marta',
            parent=None,
            published=True,
        )


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0095_auto_20250818'),
    ]

    operations = [
        migrations.RunPython(create_category_8marta, noop),
    ]

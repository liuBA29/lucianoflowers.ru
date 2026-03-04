# -*- coding: utf-8 -*-
"""
Добавить в категорию «Коллекция 8 марта» (slug 8-marta) 12 букетов с фотографиями
для блока «Сборные букеты» на /8march_design/. Картинки копируются из static.
"""
import os

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand

from stroykerbox.apps.catalog.models import Category, Product, ProductImage


CATEGORY_SLUG_8MARTA = '8-marta'
CATEGORY_NAME_8MARTA = 'Коллекция 8 марта'

STATIC_IMAGES = [
    'images/gotovaya-vitrina.png',
    'images/monoduo-bukety.png',
    'images/kompozicii.png',
    'images/wow-effect.png',
    'images/fresh-buketi.png',
    'images/podarki.png',
]

PRODUCTS_DATA = [
    {'name': 'Букет с гортензиями и розами', 'slug': 'buket-gortenzii-rozy-8m', 'sku': '8M001', 'price': 3150},
    {'name': 'Букет с розами Pink Mondal и эвкалиптом', 'slug': 'buket-pink-mondal-8m', 'sku': '8M002', 'price': 4200},
    {'name': 'Букет с пионовидными розами', 'slug': 'buket-pionovidnye-rozy-8m', 'sku': '8M003', 'price': 6000},
    {'name': 'Букет из тюльпанов к 8 марта', 'slug': 'buket-tyulpany-8marta-8m', 'sku': '8M004', 'price': 2800},
    {'name': 'Авторский букет с эвкалиптом', 'slug': 'avtorskij-buket-evkalipt-8m', 'sku': '8M005', 'price': 3500},
    {'name': 'Букет из роз и гортензий', 'slug': 'buket-rozy-gortenzii-8m', 'sku': '8M006', 'price': 4500},
    {'name': 'Сборный букет полевых цветов', 'slug': 'sbornyj-polevye-8m', 'sku': '8M007', 'price': 2200},
    {'name': 'Букет в коробке к 8 марта', 'slug': 'buket-v-korobke-8marta-8m', 'sku': '8M008', 'price': 3900},
    {'name': 'Микс букет роз и гербер', 'slug': 'miks-rozy-gerbery-8m', 'sku': '8M009', 'price': 3300},
    {'name': 'Букет с кустовыми розами', 'slug': 'buket-kustovye-rozy-8m', 'sku': '8M010', 'price': 4100},
    {'name': 'Праздничный букет к 8 марта', 'slug': 'prazdnichnyj-buket-8marta-8m', 'sku': '8M011', 'price': 2700},
    {'name': 'Букет с гортензиями и эвкалиптом', 'slug': 'buket-gortenzii-evkalipt-8m', 'sku': '8M012', 'price': 3800},
]


class Command(BaseCommand):
    help = 'Добавить 12 букетов с фото в категорию «Коллекция 8 марта» для блока Сборные букеты.'

    def handle(self, *args, **options):
        base_dir = settings.BASE_DIR
        static_dir = os.path.join(base_dir, 'static')
        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'products', 'images'), exist_ok=True)

        category = Category.objects.filter(slug=CATEGORY_SLUG_8MARTA).first()
        if not category:
            category = Category.objects.create(
                name=CATEGORY_NAME_8MARTA,
                slug=CATEGORY_SLUG_8MARTA,
                parent=None,
                published=True,
            )
            self.stdout.write(f'Создана категория: {category.name} (slug={category.slug})')
        else:
            self.stdout.write(f'Категория: {category.name}')

        created = 0
        images_attached = 0
        for i, data in enumerate(PRODUCTS_DATA):
            product = Product.objects.filter(slug=data['slug']).first()
            if product:
                if not product.images.exists():
                    static_rel = STATIC_IMAGES[i % len(STATIC_IMAGES)]
                    src = os.path.join(static_dir, static_rel)
                    if os.path.isfile(src):
                        with open(src, 'rb') as f:
                            ProductImage(product=product, position=0).image.save(
                                os.path.basename(static_rel), File(f), save=True
                            )
                        images_attached += 1
                if category not in product.categories.all():
                    product.categories.add(category)
                continue

            product = Product.objects.create(
                name=data['name'],
                slug=data['slug'],
                sku=data['sku'],
                published=True,
                price=data['price'],
            )
            product.categories.add(category)

            static_rel = STATIC_IMAGES[i % len(STATIC_IMAGES)]
            src = os.path.join(static_dir, static_rel)
            if os.path.isfile(src):
                with open(src, 'rb') as f:
                    ProductImage(product=product, position=0).image.save(
                        os.path.basename(static_rel), File(f), save=True
                    )
            created += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Создано букетов: {created}. Привязано картинок: {images_attached}. Категория: {category.name}'
            )
        )

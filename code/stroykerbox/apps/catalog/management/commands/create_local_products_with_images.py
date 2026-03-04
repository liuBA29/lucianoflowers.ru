# -*- coding: utf-8 -*-
"""
Создать пару тестовых товаров с картинками для локальной разработки.
Копирует изображения из static в media и привязывает к товарам.
"""
import os

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand

from stroykerbox.apps.catalog.models import Category, Product, ProductImage


# Картинки из static (относительно stroykerbox/static/)
STATIC_IMAGES = [
    'images/gotovaya-vitrina.png',
    'images/monoduo-bukety.png',
    'images/kompozicii.png',
    'images/wow-effect.png',
    'images/fresh-buketi.png',
    'images/podarki.png',
]


class Command(BaseCommand):
    help = 'Создать тестовые товары с картинками для локальной разработки.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=2,
            help='Сколько товаров создать (по умолчанию 2).',
        )

    def handle(self, *args, **options):
        count = options['count']
        if count < 1:
            self.stdout.write(self.style.WARNING('count должен быть >= 1.'))
            return

        base_dir = settings.BASE_DIR
        static_dir = os.path.join(base_dir, 'static')
        media_products = os.path.join(settings.MEDIA_ROOT, 'products', 'images')
        os.makedirs(media_products, exist_ok=True)

        root = Category.objects.filter(level=0, published=True).first()
        if not root:
            root = Category.objects.create(
                name='Тестовая категория',
                slug='testovaya-kategoriya',
                parent=None,
                published=True,
            )
            self.stdout.write(f'Создана категория: {root.name} (slug={root.slug})')

        products_data = [
            {'name': 'Букет из роз', 'slug': 'buket-iz-roz-local', 'sku': 'LOCAL001', 'price': 2500, 'old_price': 2990},
            {'name': 'Букет из тюльпанов', 'slug': 'buket-iz-tyulpanov-local', 'sku': 'LOCAL002', 'price': 1800, 'old_price': None},
            {'name': 'Букет из пионов', 'slug': 'buket-iz-pionov-local', 'sku': 'LOCAL003', 'price': 3200, 'old_price': 3500},
            {'name': 'Моно букет из гербер', 'slug': 'mono-buket-gerbery-local', 'sku': 'LOCAL004', 'price': 2100, 'old_price': None},
            {'name': 'Композиция из полевых цветов', 'slug': 'kompoziciya-polevye-local', 'sku': 'LOCAL005', 'price': 2800, 'old_price': 3100},
            {'name': 'Букет с эвкалиптом', 'slug': 'buket-s-evikaliptom-local', 'sku': 'LOCAL006', 'price': 1900, 'old_price': None},
            {'name': 'Свадебный букет', 'slug': 'svadebnyj-buket-local', 'sku': 'LOCAL007', 'price': 4500, 'old_price': 5000},
            {'name': 'Букет в коробке', 'slug': 'buket-v-korobke-local', 'sku': 'LOCAL008', 'price': 2200, 'old_price': None},
        ][:count]

        created = 0
        images_attached = 0
        for i, data in enumerate(products_data):
            product = Product.objects.filter(slug=data['slug']).first()
            if product:
                # Товар уже есть — привязываем картинку, если её ещё нет
                if not product.images.exists():
                    static_rel = STATIC_IMAGES[i % len(STATIC_IMAGES)]
                    src = os.path.join(static_dir, static_rel)
                    if os.path.isfile(src):
                        filename = os.path.basename(static_rel)
                        with open(src, 'rb') as f:
                            prod_img = ProductImage(product=product, position=0)
                            prod_img.image.save(filename, File(f), save=True)
                        self.stdout.write(f'  Картинка для {data["slug"]}: {filename}')
                        images_attached += 1
                    else:
                        self.stdout.write(self.style.WARNING(f'  Файл не найден: {src}'))
                else:
                    self.stdout.write(f'Товар {data["slug"]} уже есть (с картинкой), пропуск.')
                continue

            product = Product.objects.create(
                name=data['name'],
                slug=data['slug'],
                sku=data['sku'],
                published=True,
                price=data['price'],
                old_price=data.get('old_price'),
            )
            product.categories.add(root)

            # Привязываем картинки из static (по одной на товар, по кругу)
            static_rel = STATIC_IMAGES[i % len(STATIC_IMAGES)]
            src = os.path.join(static_dir, static_rel)
            if os.path.isfile(src):
                filename = os.path.basename(static_rel)
                with open(src, 'rb') as f:
                    prod_img = ProductImage(product=product, position=0)
                    prod_img.image.save(filename, File(f), save=True)
                self.stdout.write(f'  Картинка: {filename}')
            else:
                self.stdout.write(self.style.WARNING(f'  Файл не найден: {src}'))

            created += 1

        msg = f'Создано товаров: {created}.'
        if images_attached:
            msg += f' Привязано картинок к существующим: {images_attached}.'
        msg += f' Категория: {root.name}'
        self.stdout.write(self.style.SUCCESS(msg))

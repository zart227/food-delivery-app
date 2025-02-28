import os
from django.core.management.base import BaseCommand
from products.models import Product, Category
from django.utils.text import slugify
from django.conf import settings


class Command(BaseCommand):
    help = 'Populate the database with initial product data'

    def handle(self, *args, **kwargs):
        # Создаем категории
        categories = {
            'seafood': {
                'name': 'Морепродукты',
                'slug': 'seafood',
                'description': 'Блюда из морепродуктов'
            },
            'meat': {
                'name': 'Мясные блюда',
                'slug': 'meat',
                'description': 'Блюда из мяса'
            },
            'salads': {
                'name': 'Салаты',
                'slug': 'salads',
                'description': 'Свежие салаты'
            },
            'soups': {
                'name': 'Супы',
                'slug': 'soups',
                'description': 'Первые блюда'
            },
            'vegetarian': {
                'name': 'Вегетарианские блюда',
                'slug': 'vegetarian',
                'description': 'Блюда без мяса'
            }
        }

        created_categories = {}
        for slug, cat_data in categories.items():
            category, created = Category.objects.get_or_create(
                slug=slug,
                defaults=cat_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created category: {category.name}"))
            created_categories[slug] = category

        # Данные товаров с указанием категорий
        goods = [
            {
                'title': 'Устрицы по рокфеллеровски',
                'description': 'Свежайшие устрицы, запечённые под сливочным соусом с зеленью и сыром. Блюдо для истинных гурманов, которое подается с ломтиками лимона.',
                'price': 2700,
                'image': 'products/image0.png',
                'category': 'seafood',
                'is_spicy': False,
                'is_vegetarian': False
            },
            {
                'title': 'Свиные ребрышки на гриле с зеленью',
                'description': 'Сочные свиные ребрышки, приготовленные на гриле, подаются с ароматной зеленью и чесночным соусом. Идеальный выбор для любителей мяса.',
                'price': 1600,
                'image': 'products/image1.png',
                'category': 'meat',
                'is_spicy': True,
                'is_vegetarian': False
            },
            {
                'title': 'Креветки по-королевски в лимонном соке',
                'description': 'Крупные креветки, замаринованные в свежем лимонном соке и приготовленные до идеальной текстуры. Подаются с соусом из пряных трав.',
                'price': 1820,
                'image': 'products/image2.png',
                'category': 'seafood',
                'is_spicy': False,
                'is_vegetarian': False
            },
            {
                'title': 'Мидии в белом вине с чесноком',
                'description': 'Мидии, приготовленные в белом вине с добавлением чеснока, петрушки и сливочного масла. Блюдо обладает утончённым вкусом и ароматом моря.',
                'price': 2200,
                'image': 'products/image3.png',
                'category': 'seafood',
                'is_spicy': False,
                'is_vegetarian': False
            },
            {
                'title': 'Стейк рибай с соусом чимичурри',
                'description': 'Мраморный стейк рибай, приготовленный до желаемой степени прожарки. Подается с пикантным соусом чимичурри, на основе свежей зелени, чеснока и оливкового масла.',
                'price': 3500,
                'image': 'products/image4.png',
                'category': 'meat',
                'is_spicy': True,
                'is_vegetarian': False
            },
            {
                'title': 'Каре ягнёнка с розмарином',
                'description': 'Нежное каре ягнёнка, обжаренное до золотистой корочки и приправленное свежим розмарином. Подается с соусом на основе красного вина.',
                'price': 3800,
                'image': 'products/image5.png',
                'category': 'meat',
                'is_spicy': False,
                'is_vegetarian': False
            },
            {
                'title': 'Сашими из лосося',
                'description': 'Тонкие ломтики свежего лосося, нарезанные вручную. Подаются с соевым соусом, васаби и маринованным имбирем для утончённого вкусового удовольствия.',
                'price': 2400,
                'image': 'products/image6.png',
                'category': 'seafood',
                'is_spicy': True,
                'is_vegetarian': False
            },
            {
                'title': 'Том ям с морепродуктами',
                'description': 'Классический тайский суп с креветками, мидиями, грибами и ароматными специями. Пикантный вкус усиливается соком лайма и кокосовым молоком.',
                'price': 1500,
                'image': 'products/image7.png',
                'category': 'soups',
                'is_spicy': True,
                'is_vegetarian': False
            },
            {
                'title': 'Цезарь с креветками',
                'description': 'Классический салат с хрустящими листьями ромена, золотистыми креветками, домашними гренками и пармезаном, заправленный оригинальным соусом Цезарь.',
                'price': 1300,
                'image': 'products/image8.png',
                'category': 'salads',
                'is_spicy': False,
                'is_vegetarian': False
            },
            {
                'title': 'Тартар из тунца с авокадо',
                'description': 'Свежий тунец мелко нарезан и подан с кубиками спелого авокадо. Завершает блюдо пикантный соус терияки и кунжутные семена.',
                'price': 2100,
                'image': 'products/image9.png',
                'category': 'seafood',
                'is_spicy': False,
                'is_vegetarian': False
            },
            {
                'title': 'Гребешки на гриле с лимоном',
                'description': 'Морские гребешки, обжаренные на гриле до золотистой корочки, подаются с ломтиками лимона и свежими травами. Настоящий деликатес.',
                'price': 3200,
                'image': 'products/image10.png',
                'category': 'seafood',
                'is_spicy': False,
                'is_vegetarian': False
            },
            {
                'title': 'Дорада с ароматными травами',
                'description': 'Свежая дорада, запечённая с тимьяном, розмарином и лимоном. Блюдо отличается нежным вкусом и утончённым ароматом.',
                'price': 2900,
                'image': 'products/image11.png',
                'category': 'seafood',
                'is_spicy': False,
                'is_vegetarian': False
            },
            {
                'title': 'Филе лосося на пару с соусом юдзу',
                'description': 'Лосось, приготовленный на пару для сохранения всех полезных свойств, подаётся с освежающим соусом из японского цитруса юдзу.',
                'price': 3100,
                'image': 'products/image12.png',
                'category': 'seafood',
                'is_spicy': False,
                'is_vegetarian': False
            },
            {
                'title': 'Паста с мидиями и креветками',
                'description': 'Домашняя паста, приготовленная со сливочно-чесночным соусом, украшенная мидиями и креветками. Завершает вкус тёртый пармезан.',
                'price': 1800,
                'image': 'products/image13.png',
                'category': 'seafood',
                'is_spicy': False,
                'is_vegetarian': False
            },
            {
                'title': 'Рататуй с овощами',
                'description': 'Традиционное французское блюдо из свежих овощей, запечённых с травами Прованса. Яркий вкус и аппетитный аромат.',
                'price': 1100,
                'image': 'products/image14.png',
                'category': 'vegetarian',
                'is_spicy': False,
                'is_vegetarian': True
            },
            {
                'title': 'Стейк из тунца с кунжутом',
                'description': 'Нежное филе тунца, обжаренное в кунжутной панировке. Подаётся с пикантным соусом терияки для усиления вкусовых акцентов.',
                'price': 3500,
                'image': 'products/image15.png',
                'category': 'seafood',
                'is_spicy': True,
                'is_vegetarian': False
            },
        ]

        for good in goods:
            category = created_categories[good['category']]

            # Создаём или обновляем товар
            product, created = Product.objects.update_or_create(
                title=good['title'],
                defaults={
                    'description': good['description'],
                    'price': good['price'],
                    'image': good['image'],
                    'category': category,
                    'is_spicy': good['is_spicy'],
                    'is_vegetarian': good['is_vegetarian']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created: {product.title}"))
            else:
                self.stdout.write(self.style.WARNING(f"Updated: {product.title}"))

from django.core.management.base import BaseCommand, CommandError
from django.utils.text import slugify

from faker import Faker

from apps.catalog.models import Catalog, Product, Image

class Command(BaseCommand):
    help = 'Create products -c <count> -lang <language>'

    def add_arguments(self, parser):
        parser.add_argument('-c', '--count', type=int, default=10)
        parser.add_argument('-lang', '--language', type=str, default='en_US')

    def handle(self, *args, **options):
        count = options['count']
        language = options['language']
        fake = Faker(language)

        for _ in range(count):
            name = fake.text(20)
            product = Product.objects.create(
                name=name,
                slug=slugify(name),
                description=fake.text(200),
                quantity=fake.random_int(0, 100),
                price=fake.random_int(10, 1000),
            )
            product.category.add(Catalog.objects.order_by('?').first())
            product.save()

            image_random = Image.objects.order_by('?').first()
            Image.objects.create(
                product=product,
                image=image_random.image,
                is_main=True,
            )
            self.stdout.write(self.style.SUCCESS(f'Product {product.name} created'))
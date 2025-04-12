from django.core.management import BaseCommand
from recipes.models import Tag


class Command(BaseCommand):
    def handle(self, *args, **options):
        tags_list = [
            {'name': 'Завтрак',
             'color': '#FF8C00',
             'slug': 'breakfast'},
            {'name': 'Обед',
             'color': '#8B0000',
             'slug': 'lunch'},
            {'name': 'Ужин',
             'color': '#CD5C5C',
             'slug': 'dinner'}
        ]
        for row in tags_list:
            tag = Tag(name=row['name'], color=row['color'], slug=row['slug'])
            tag.save()
        self.stdout.write(self.style.SUCCESS('Successfully add tags'))

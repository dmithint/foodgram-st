import os
import json
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foodgram_backend.settings')
django.setup()

from recipes.models import Ingredient

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as jsonfile:
        data = json.load(jsonfile)
        for item in data:
            Ingredient.objects.get_or_create(**item)

def main():
    file_path = os.getenv('DATA_FILE', 'data/ingredients.json')
    load_json(file_path)

if __name__ == '__main__':
    main()

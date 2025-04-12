from django.contrib.auth import password_validation
from django.db import transaction
from django.db.models import F
from drf_extra_fields.fields import Base64ImageField
from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag
from rest_framework import serializers
from users.models import Subscription, User


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для тегов"""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для ингредиентов"""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class UserGetSerializer(serializers.ModelSerializer):
    """Сериализатор для вывода данных о пользователях"""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'password', 'is_subscribed')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def get_is_subscribed(self, obj):
        if self.context.get('request') and self.context[
            'request'].user.is_authenticated:
            return obj.following.filter(user=self.context['request'].user,
                                        author=obj).exists()
        return False


class UserPostSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователя"""

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class PasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)
    current_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        password_validation.validate_password(value)
        return value

    def update(self, instance, validated_data):
        if not instance.check_password(validated_data['current_password']):
            raise serializers.ValidationError('Неверный пароль')
        if validated_data['current_password'] == validated_data[
            'new_password']:
            raise serializers.ValidationError(
                'Новый пароль должен отличаться от старого')
        instance.set_password(validated_data['new_password'])
        instance.save()
        return validated_data


class RecipeMinifiedSerializer(serializers.ModelSerializer):
    """Вывод рецепта в сокращенном виде"""
    image = Base64ImageField(use_url=True)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscriptionSerializer(serializers.ModelSerializer):
    recipes = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    email = serializers.ReadOnlyField(source='author.email')
    id = serializers.ReadOnlyField(source='author.id')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')

    class Meta:
        model = Subscription
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_is_subscribed(self, obj):
        if self.context.get('request') and self.context[
            'request'].user.is_authenticated:
            return Subscription.objects.filter(
                user=self.context['request'].user, author=obj.author).exists()
        return False

    def get_recipes_count(self, obj):
        return obj.author.recipes.count()

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        recipes_list = obj.author.recipes.all()
        if limit:
            recipes_list = recipes_list[:int(limit)]
        return RecipeMinifiedSerializer(recipes_list, many=True).data


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для вывода рецепта"""
    image = Base64ImageField(use_url=True)
    tags = TagSerializer(many=True)
    author = UserGetSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time')

    def get_ingredients(self, obj):
        ingredients = obj.ingredients.values('id', 'name', 'measurement_unit',
                                             amount=F(
                                                 'recipe_ingredients__amount'))
        return ingredients

    def get_is_favorited(self, obj):
        if self.context.get('request') and self.context[
            'request'].user.is_authenticated:
            return (self.context[
                    'request'].user.is_authenticated and obj.favorite.filter(
                    user=self.context['request'].user, recipe=obj).exists())
        return False

    def get_is_in_shopping_cart(self, obj):
        if self.context.get('request') and self.context[
            'request'].user.is_authenticated:
            return (self.context[
                    'request'].user.is_authenticated and obj.shopping.filter(
                    user=self.context['request'].user, recipe=obj).exists())
        return False


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Сериализотор для ингредиентов при создании/редактировании рецептов"""
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField(write_only=True)

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')


class RecipePostSerializer(serializers.ModelSerializer):
    """Сериализатор для соднания и редактирования рецепта"""
    image = Base64ImageField(use_url=True)
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(),
                                              many=True)
    ingredients = RecipeIngredientSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ('id', 'ingredients', 'tags', 'image', 'name', 'text',
                  'cooking_time')

    def validate(self, data):
        ingredients = data.get('ingredients')
        ingredient_list = []
        for ingredient in ingredients:
            id = ingredient.get('id').id
            if not Ingredient.objects.filter(id=id).exists():
                raise serializers.ValidationError('Такого инградиента нет')
            if id in ingredient_list:
                raise serializers.ValidationError(
                    'Игредиенты не должны повторяться')
            ingredient_list.append(id)
        tags = data.get('tags')
        tag = tags[0]
        for tag in tags:
            id = tag.pk
            if not Tag.objects.filter(id=id).exists():
                raise serializers.ValidationError('Такого тэга нет')
        amount = int(ingredient.get('amount'))
        if amount < 1:
            raise serializers.ValidationError(
                'Количество инградиентов не должно быть меньше 1')
        cooking_time = data.get('cooking_time')
        if cooking_time < 1:
            raise serializers.ValidationError(
                'Время приготовления должно быть не меньше 1 минуты')
        return data

    def validate_recipe_exist(self, data):
        author = self.context['request'].user
        name = data.get('name')
        if Recipe.objects.filter(author=author, name=name).exists():
            raise serializers.ValidationError('рецепт уже существует')

    @transaction.atomic(durable=True)
    def create(self, validated_data):
        """Создание рецепта"""
        self.validate_recipe_exist(validated_data)
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        for ingredient in ingredients:
            current_ingredient = ingredient.get('id')
            amount = ingredient.get('amount')
            RecipeIngredient.objects.create(recipe=recipe,
                                            ingredient=current_ingredient,
                                            amount=amount)
        recipe.tags.set(tags)
        return recipe

    @transaction.atomic(durable=True)
    def update(self, instance, validated_data):
        """Обновление рецепта"""
        if 'tags' in validated_data:
            tags_data = validated_data.pop('tags')
            instance.tags.clear()
            instance.tags.set(tags_data)
        if 'ingredients' in validated_data:
            ingredients_data = validated_data.pop('ingredients')
            RecipeIngredient.objects.filter(recipe__id=instance.id).delete()
            for ingredient in ingredients_data:
                current_ingredient = ingredient.get('id')
                amount = ingredient.get('amount')
                RecipeIngredient.objects.create(recipe=instance,
                                                ingredient=current_ingredient,
                                                amount=amount)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        serializer = RecipeSerializer(instance)
        return serializer.data

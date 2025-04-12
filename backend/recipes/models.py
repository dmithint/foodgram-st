from django.core.validators import MinValueValidator
from django.db import models
from users.models import User


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name='Автор рецепта',
        related_name='recipes',
        on_delete=models.CASCADE
    )
    name = models.CharField(
        verbose_name='Название рецепта',
        max_length=200
    )
    image = models.ImageField(
        verbose_name='Фото рецепта',
        upload_to='recipe/images/'
    )
    text = models.TextField(
        verbose_name='Описание')
    ingredients = models.ManyToManyField(
        'Ingredient',
        verbose_name='Ингредиенты',
        through='RecipeIngredient'
    )
    tags = models.ManyToManyField(
        'Tag',
        verbose_name='Теги'
    )
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления',
        default=1,
        validators=[MinValueValidator(1), ]
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'name',),
                name='unique_author_name'
            )]

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Название тега',
        unique=True,
        max_length=200
    )
    color = models.CharField(
        verbose_name='Цвет',
        default='#ffffff',
        max_length=7,
        unique=True
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        max_length=200,
        unique=True
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Название ингредиента',
        max_length=200
    )
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=200
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=('name', 'measurement_unit',),
                name='unique_name_unit'
            )]

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ингредиент',
        related_name='recipe_ingredients',
        on_delete=models.PROTECT
    )
    amount = models.IntegerField(
        verbose_name='Количество',
        validators=[MinValueValidator(1, message='Минимальное значение 1'), ]
    )

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиента'
        constraints = [
            models.UniqueConstraint(
                fields=('recipe', 'ingredient',),
                name='unique_recipe_ingredient'
            )]

    def __str__(self):
        return f'{self.ingredient} {self.amount}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        related_name='favorite',
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='избранный рецепт',
        related_name='favorite',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Избранные рецепты'
        verbose_name_plural = 'Избранные рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_user_recipe'
            )]

    def __str__(self):
        return f'{self.recipe}, {self.user}'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Составитель списка покупок',
        related_name='shopping',
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт в списке покупок',
        related_name='shopping',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_favorite'
            )]

    def __str__(self):
        return f'{self.recipe}, {self.user}'

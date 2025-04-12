from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingCart, Tag)
from users.models import Subscription, User


class IngredientsInLine(admin.TabularInline):
    model = RecipeIngredient
    min_num = 1
    extra = 3


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ('pk', 'first_name', 'last_name', 'username', 'email',)
    search_fields = ('email', 'username',)
    list_filter = ('email', 'username',)
    ordering = ('id',)
    empty_value_display = '-пусто-'


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'author',)
    list_filter = ('user', 'author',)
    search_fields = ('user', 'author',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [IngredientsInLine]
    list_display = ('pk', 'author', 'name', 'in_favorite',)
    fields = (
        ('name', 'tags',),
        ('author', 'cooking_time',),
        ('image',),
        ('text',),
    )
    search_fields = ('author', 'name',)
    list_filter = ('author', 'name',)

    def in_favorite(self, obj):
        return obj.favorite.all().count()

    in_favorite.short_description = 'В избранном'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug',)
    list_filter = ('name',)
    list_editable = ('color',)
    empty_value_display = '-пусто-'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    list_filter = ('name',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)
    list_filter = ('user__username', 'recipe__name',)
    search_filter = ('user__username', 'recipe__name',)


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)
    list_filter = ('user', 'recipe',)
    search_fields = ('user',)

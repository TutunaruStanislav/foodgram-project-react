from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User
from .models import (
    Favorite, Follow, Ingredient, IngredientAmount, Purchase, Recipe, Tag
)


class IngredientsInline(admin.TabularInline):
    model = IngredientAmount
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'amount_favorites',)
    inlines = (IngredientsInline,)
    list_filter = ('author', 'name', 'tags',)

    def amount_favorites(self, obj):
        return obj.recipe.count()

    amount_favorites.short_description = 'Добавлено в избранное'


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name',)
    search_fields = ('username', 'email',)
    list_filter = ('username', 'email',)
    empty_value_display = '-пусто-'


@admin.register(Favorite, Purchase)
class BaseUserRecipeAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)

    def user(self, obj):
        return obj.user.first_name

    user.short_description = 'Пользователь'

    def recipe(self, obj):
        return obj.recipe.name

    recipe.short_description = 'Рецепт'


@admin.register(Follow)
class FollowAdmin(BaseUserRecipeAdmin):
    list_display = ('user', 'author',)

    def author(self, obj):
        return obj.author.first_name

    author.short_description = 'Автор'


@admin.register(Ingredient)
class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)

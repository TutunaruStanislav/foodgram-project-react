from django.contrib import admin
from users.models import User

from .models import (Favorite, Follow, Ingredient, IngredientAmount, Purchase,
                     Recipe, Tag)


class IngredientsInline(admin.TabularInline):
    model = IngredientAmount
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'amount_favorites',)
    inlines = (IngredientsInline,)
    list_filter = ('author', 'name', 'tags')

    def amount_favorites(self, obj):
        if obj.recipe.count():
            return obj.recipe.count()

        return None

    amount_favorites.short_description = 'Добавлено в избранное'


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name',)
    search_fields = ('username', 'email',)
    list_filter = ('username', 'email',)
    empty_value_display = '-пусто-'

    def save_model(self, request, obj, form, change):
        if obj.pk:
            obj.set_password(obj.password)
        obj.save()


class BaseUserRecipeAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)

    def user(self, obj):
        return obj.user.first_name

    user.short_description = 'Пользователь'

    def recipe(self, obj):
        return obj.recipe.name

    recipe.short_description = 'Рецепт'


class FollowAdmin(BaseUserRecipeAdmin):
    list_display = ('user', 'author',)

    def author(self, obj):
        return obj.author.first_name

    author.short_description = 'Автор'


admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Favorite, BaseUserRecipeAdmin)
admin.site.register(Purchase, BaseUserRecipeAdmin)
admin.site.register(User, UserAdmin)
from rest_framework.validators import ValidationError

from service.models import Ingredient, Tag


def validate_ingredients(ingredients):
    if not ingredients or len(ingredients) < 1:
        raise ValidationError({'ingredients': ['Обязательное поле']})

    ingredients_ids = []
    for ingredient in ingredients:
        pk = ingredient.get('id')
        if not pk or not Ingredient.objects.filter(id=pk).exists():
            raise ValidationError({'ingredients': ['Ингредиент не найден']})

        if pk in ingredients_ids:
            raise ValidationError(
                {'ingredients': ['Ингредиент с таким id уже передан']})
        ingredients_ids.append(pk)

        if int(ingredient.get('amount')) < 1:
            raise ValidationError({'amount': ['Минимальное количество - 1']})

    return ingredients


def validate_tags(tags):
    if not tags or len(tags) < 1:
        raise ValidationError({'tags': ['Обязательное поле']})

    for tag in tags:
        if not Tag.objects.filter(id=tag).exists():
            raise ValidationError({'tags': ['Тэг не найден']})

    return tags

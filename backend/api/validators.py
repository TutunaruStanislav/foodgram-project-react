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


def validate_subscribe(context):
    if context.get('request').method == 'POST':
        if context.get('request').user == context.get('author'):
            raise ValidationError({'errors': ['Нельзя подписаться на себя']})

        if context.get('subscription').exists():
            raise ValidationError(
                {'errors': ['Вы уже подписаны на пользователя']})

    if context.get('request').method == 'DELETE':
        if not context.get('subscription').exists():
            raise ValidationError(
                {'errors': ['Вы уже отписались от пользователя']})

    return context


def validate_favorite_purchase(context):
    if context.get('self'):
        if context.get('self').model.objects.filter(
                user=context.get('self').request.user,
                recipe__id=context.get('self').kwargs['pk']).exists():
            raise ValidationError({'errors': 'Рецепт ранее был добавлен'})
    else:
        if not context.get('obj').exists():
            raise ValidationError({'errors': 'Рецепт уже был удален'})

    return context

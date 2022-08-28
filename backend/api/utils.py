from django.db.models import Sum

from service.models import IngredientAmount


def render_purchase_list(request):
    purchase_list = []
    ingredients = IngredientAmount.objects.filter(
        recipe__purchase__user=request.user).values(
        'ingredient__name', 'ingredient__measurement_unit').order_by(
        'ingredient__name').annotate(total=Sum('amount'))

    for ingredient in ingredients:
        purchase_list.append(
            f'{ingredient["ingredient__name"]} - '
            f'{ingredient["total"]} '
            f'{ingredient["ingredient__measurement_unit"]}\n'
        )

    return purchase_list

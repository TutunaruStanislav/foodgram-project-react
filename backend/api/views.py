from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin, RetrieveModelMixin)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from service.models import (Favorite, Follow, Ingredient, IngredientAmount,
                            Purchase, Recipe, Tag)
from users.models import User

from .filters import IngredientFilter, RecipeFilter
from .permissions import IsAuthorOrReadOnly
from .serializers import (FollowSerializer, IngredientSerializer,
                          RecipeGetSerializer, RecipeSerializer, TagSerializer,
                          UserSerializer)


class UserListCreateViewSet(ListModelMixin, RetrieveModelMixin,
                            CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = UserSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        user_id = self.kwargs.get('pk')
        if user_id:
            if user_id == 'me':
                user_id = self.request.user.id
            return get_object_or_404(User, pk=user_id)

        return User.objects.all()

    def retrieve(self, request, *args, **kwargs):
        serializer = UserSerializer(self.get_queryset())
        return Response(serializer.data)


class TagViewSet(ListModelMixin, RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny, ]
    pagination_class = None


class IngredientViewSet(ListModelMixin, RetrieveModelMixin,
                        viewsets.GenericViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [AllowAny, ]
    pagination_class = None
    filter_class = IngredientFilter
    filter_backends = [DjangoFilterBackend, ]
    search_fields = ('name', )


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated, ]

    @action(detail=True, methods=['post', 'delete'])
    def subscribe(self, request, pk=None):
        author = get_object_or_404(User, id=pk)
        subscription = Follow.objects.filter(author=author, user=request.user)

        if request.method == 'POST':
            if request.user == author:
                return Response(
                    {'errors': 'Нельзя подписаться на себя'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if subscription.exists():
                return Response(
                    {'errors': 'Вы уже подписаны на пользователя'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            follow = Follow.objects.create(author=author, user=request.user)
            serializer = FollowSerializer(follow, context={'request': request})

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            if not subscription.exists():
                return Response(
                    {'errors': 'Вы уже отписались от пользователя'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            subscription.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filter_class = RecipeFilter
    filter_backends = [DjangoFilterBackend, ]
    permission_classes = [IsAuthorOrReadOnly, ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FavoritePurchaseViewSet(CreateModelMixin,
                              DestroyModelMixin,
                              viewsets.GenericViewSet):
    model = None
    permission_classes = [IsAuthenticated, ]

    def create(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if self.model.objects.filter(user=self.request.user,
                                     recipe__id=pk).exists():
            return Response({
                'errors': 'Рецепт ранее был добавлен'
            }, status=status.HTTP_400_BAD_REQUEST)

        recipe = get_object_or_404(Recipe, id=pk)
        self.model.objects.create(user=self.request.user, recipe=recipe)
        serializer = RecipeGetSerializer(recipe)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        obj = self.model.objects.filter(user=self.request.user,
                                        recipe__id=kwargs.get('pk'))
        if not obj.exists():
            return Response({
                'errors': 'Рецепт уже был удален'
            }, status=status.HTTP_400_BAD_REQUEST)

        obj.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class FavoriteViewSet(FavoritePurchaseViewSet):
    queryset = Favorite.objects.all()
    serializer_class = RecipeGetSerializer
    model = Favorite


class PurchaseViewSet(FavoritePurchaseViewSet):
    queryset = Purchase.objects.all()
    serializer_class = RecipeGetSerializer
    model = Purchase

    @action(detail=True, methods=['GET'])
    def purchase_list(self, request):
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

        response = HttpResponse(purchase_list, 'Content-Type: text/plain')
        response['Content-Disposition'] = ('attachment; '
                                           'filename="PurchaseList.txt"')

        return response

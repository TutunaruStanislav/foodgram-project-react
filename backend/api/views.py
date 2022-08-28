from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin, RetrieveModelMixin
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from recipes.models import (
    Favorite, Follow, Ingredient, Purchase, Recipe, Tag
)
from users.models import User
from .filters import IngredientFilter, RecipeFilter
from .mixins import CreateDestroyMixin, ListRetrieveMixin
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    FavoritePurchaseSerializer, FollowSerializer, IngredientSerializer,
    RecipeGetSerializer, RecipeSerializer, TagSerializer, UserSerializer
)
from .utils import render_purchase_list


class UserListCreateViewSet(ListModelMixin,
                            RetrieveModelMixin,
                            CreateModelMixin,
                            viewsets.GenericViewSet):
    serializer_class = UserSerializer
    permission_classes = (AllowAny, )

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


class TagViewSet(ListRetrieveMixin):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny, )
    pagination_class = None


class IngredientViewSet(ListRetrieveMixin):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny, )
    filter_backends = (IngredientFilter,)
    pagination_class = None
    search_fields = ('^name',)


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated, )

    @action(detail=True, methods=['post', 'delete'])
    def subscribe(self, request, pk=None):
        author = get_object_or_404(User, id=pk)
        subscription = Follow.objects.filter(author=author, user=request.user)
        serializer = FollowSerializer(data={}, context={
            'author': author,
            'subscription': subscription,
            'request': request,
        })

        if serializer.is_valid(raise_exception=True):
            if request.method == 'POST':
                follow = Follow.objects.create(author=author,
                                               user=request.user)
                serializer = FollowSerializer(follow, context={
                    'request': request
                })

                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)

            subscription.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filter_class = RecipeFilter
    filter_backends = (DjangoFilterBackend, )
    permission_classes = (IsAuthorOrReadOnly, )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FavoritePurchaseViewSet(CreateDestroyMixin):
    model = None
    permission_classes = (IsAuthenticated, )

    def create(self, request, *args, **kwargs):
        serializer = FavoritePurchaseSerializer(data={},
                                                context={'self': self})
        if serializer.is_valid(raise_exception=True):
            recipe = get_object_or_404(Recipe, id=kwargs.get('pk'))
            self.model.objects.create(user=self.request.user, recipe=recipe)
            serializer = RecipeGetSerializer(recipe)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        obj = self.model.objects.filter(user=self.request.user,
                                        recipe__id=kwargs.get('pk'))
        serializer = FavoritePurchaseSerializer(data={}, context={'obj': obj})
        if serializer.is_valid(raise_exception=True):
            obj.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_400_BAD_REQUEST)


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
        response = HttpResponse(render_purchase_list(request),
                                'Content-Type: text/plain')
        response['Content-Disposition'] = ('attachment; '
                                           'filename="PurchaseList.txt"')

        return response

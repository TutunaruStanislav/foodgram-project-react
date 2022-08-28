from django.urls import include, path
from djoser.views import UserViewSet
from rest_framework import routers

from .views import (
    FavoriteViewSet, FollowViewSet, IngredientViewSet, PurchaseViewSet,
    RecipeViewSet, TagViewSet, UserListCreateViewSet
)

app_name = 'api'

router = routers.DefaultRouter()
router.register('users', UserListCreateViewSet, basename='users')
router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('users/set_password/', UserViewSet.as_view({'post': 'set_password'}),
         name='set_password'),
    path('users/subscriptions/', FollowViewSet.as_view({'get': 'list'}),
         name='get_subscriptions'),
    path('users/<int:pk>/subscribe/',
         FollowViewSet.as_view({'post': 'subscribe', 'delete': 'subscribe'}),
         name='add_subscribe'),
    path('recipes/<int:pk>/favorite/',
         FavoriteViewSet.as_view({'post': 'create', 'delete': 'destroy'}),
         name='add_to_favorite'),
    path('recipes/<int:pk>/shopping_cart/',
         PurchaseViewSet.as_view({'post': 'create', 'delete': 'destroy'}),
         name='add_to_purchase'),
    path('recipes/download_shopping_cart/',
         PurchaseViewSet.as_view({'get': 'purchase_list'}),
         name='purchase_list'),
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]

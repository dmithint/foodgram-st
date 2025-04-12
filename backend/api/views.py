from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from api.filters import IngredientFilter, RecipeFilter
from api.pagination import CustomPagination
from api.permissions import IsAuthorOrReadOnly
from api.serializers import (IngredientSerializer, PasswordSerializer,
                             RecipeMinifiedSerializer, RecipePostSerializer,
                             RecipeSerializer, SubscriptionSerializer,
                             TagSerializer, UserGetSerializer,
                             UserPostSerializer)
from api.utils import create_pdf
from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingCart, Tag)
from users.models import Subscription, User


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Получить список ингредиентов"""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
    pagination_class = None


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Получить список тегов"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет для рецептов"""
    queryset = Recipe.objects.all()
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    permission_classes = (IsAuthorOrReadOnly,)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeSerializer
        return RecipePostSerializer

    def perform_create(self, serializer):
        """Создание рецепта"""
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['POST', 'DELETE'],
            pagination_class=None,
            permission_classes=(IsAuthenticated,))
    def favorite(self, request, **kwargs):
        """Добаление и удаление рецепта в/из спискок избранного"""
        user = request.user
        id = self.kwargs.get('pk')
        recipe = get_object_or_404(Recipe, id=id)
        if request.method == 'POST':
            if Favorite.objects.filter(user=user, recipe=recipe).exists():
                return Response(status=status.HTTP_400_BAD_REQUEST)
            Favorite.objects.create(user=user, recipe=recipe)
            serializer = RecipeMinifiedSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if not Favorite.objects.filter(user=user, recipe=recipe).exists():
                return Response(status=status.HTTP_400_BAD_REQUEST)
            Favorite.objects.filter(user=user, recipe=recipe).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['POST', 'DELETE'],
            pagination_class=None,
            permission_classes=(IsAuthenticated,))
    def shopping_cart(self, request, **kwargs):
        """Добавление и удаление рецепта в/из список покупок"""
        user = request.user
        id = self.kwargs.get('pk')
        recipe = get_object_or_404(Recipe, id=id)
        if request.method == 'POST':
            if ShoppingCart.objects.filter(user=user, recipe=recipe).exists():
                return Response(status=status.HTTP_400_BAD_REQUEST)
            ShoppingCart.objects.create(user=user, recipe=recipe)
            serializer = RecipeMinifiedSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if not ShoppingCart.objects.filter(user=user,
                                               recipe=recipe).exists():
                return Response(status=status.HTTP_400_BAD_REQUEST)
            ShoppingCart.objects.filter(user=user, recipe=recipe).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['GET'],
            permission_classes=(IsAuthenticated,))
    def download_shopping_cart(self, request):
        """Вывод списка покупок в pdf файл"""
        user = request.user
        ingredients = RecipeIngredient.objects.filter(
            recipe__shopping__user=user).values(
            'ingredient__name', 'ingredient__measurement_unit').annotate(
            ingredient_amount=Sum('amount'))
        file = create_pdf(ingredients)
        response = HttpResponse(content_type='application/pdf',
                                status=status.HTTP_200_OK)
        response.write(bytes(file))
        return response


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для юзера"""
    queryset = User.objects.all()
    serializer_class = UserGetSerializer
    permission_classes = (AllowAny,)
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserGetSerializer
        if self.request.method == 'POST':
            return UserPostSerializer

    @action(detail=False, methods=['get'],
            pagination_class=None,
            permission_classes=(IsAuthenticated,))
    def me(self, request):
        """Вывод профиля текущего пользователя"""
        serializer = UserGetSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'],
            permission_classes=(IsAuthenticated,))
    def set_password(self, request):
        """Изменить пароль"""
        serializer = PasswordSerializer(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('Пароль успешно изменен',
                            status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'],
            permission_classes=(IsAuthenticated,))
    def subscriptions(self, request):
        """Список пользователей, на которых подписан текущий пользователь"""
        user = request.user
        queryset = user.follower.all()
        page = self.paginate_queryset(queryset)
        serializer = SubscriptionSerializer(page, many=True,
                                            context={'request': request})
        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=['POST', 'DELETE'],
            pagination_class=None,
            permission_classes=(IsAuthenticated,))
    def subscribe(self, request, **kwargs):
        """Подписаться или отписаться от пользователя"""
        user = request.user
        id = self.kwargs.get('pk')
        author = get_object_or_404(User, id=id)
        if request.method == 'POST':
            if author == user or Subscription.objects.filter(
                    user=user, author=author).exists():
                return Response(status=status.HTTP_400_BAD_REQUEST)
            queryset = Subscription.objects.create(user=user, author=author)
            serializer = SubscriptionSerializer(queryset, data=request.data,
                                                context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        if request.method == 'DELETE':
            get_object_or_404(Subscription, user=user, author=author).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

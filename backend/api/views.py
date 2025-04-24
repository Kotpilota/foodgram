from django.db.models import Prefetch
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from recipes.models import (
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredient,
    ShoppingCart,
    Tag,
)
from users.models import Subscription, User

from .mixins import CollectionActionMixin, SubscriptionActionMixin
from .pagination import CustomPagination
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    IngredientSerializer,
    RecipeCreateSerializer,
    RecipeGetShortLinkSerializer,
    RecipeMinifiedSerializer,
    RecipeSerializer,
    SetAvatarSerializer,
    SetPasswordSerializer,
    TagSerializer,
    UserSerializer,
    UserWithRecipesSerializer,
)


class UserViewSet(DjoserUserViewSet, SubscriptionActionMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.action == 'retrieve':
            return [permissions.AllowAny()]
        return super().get_permissions()

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def subscriptions(self, request):
        user = request.user
        subscriptions = User.objects.filter(subscribers__user=user)
        page = self.paginate_queryset(subscriptions)
        serializer = UserWithRecipesSerializer(
            page, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def subscribe(self, request, id=None):
        return self.handle_subscription_action(
            request=request,
            user_id=id,
            model_class=Subscription,
            serializer_class=UserWithRecipesSerializer
        )

    @action(
        detail=False,
        methods=['post'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def set_password(self, request):
        user = request.user
        serializer = SetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        current_password = serializer.validated_data['current_password']
        new_password = serializer.validated_data['new_password']

        if not user.check_password(current_password):
            return Response(
                {'current_password': ['Неверный пароль']},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(new_password)
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['put', 'delete'],
        permission_classes=[permissions.IsAuthenticated],
        url_path='me/avatar'
    )
    def avatar(self, request):
        user = request.user

        if request.method == 'PUT':
            if 'avatar' not in request.data:
                return Response(
                    {'avatar': ['Обязательное поле.']},
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer = SetAvatarSerializer(
                user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        if request.method == 'DELETE':
            if user.avatar:
                user.avatar.delete()
                user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get('name')

        if name:
            queryset = queryset.filter(name__istartswith=name)

        return queryset


class RecipeViewSet(viewsets.ModelViewSet, CollectionActionMixin):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthorOrReadOnly]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = super().get_queryset()

        author = self.request.query_params.get('author')
        tags = self.request.query_params.getlist('tags')
        is_favorited = self.request.query_params.get('is_favorited')
        is_in_shopping_cart = self.request.query_params.get(
            'is_in_shopping_cart')

        if author:
            queryset = queryset.filter(author_id=author)

        if tags:
            queryset = queryset.filter(tags__slug__in=tags).distinct()

        if is_favorited and self.request.user.is_authenticated:
            queryset = queryset.filter(favorited_by__user=self.request.user)

        if is_in_shopping_cart and self.request.user.is_authenticated:
            queryset = queryset.filter(
                in_shopping_cart__user=self.request.user)

        return queryset

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return RecipeCreateSerializer
        return RecipeSerializer

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def favorite(self, request, pk=None):
        return self.handle_collection_action(
            request=request,
            pk=pk,
            model_class=Favorite,
            success_message='Рецепт успешно добавлен в избранное',
            error_exists_message='Рецепт уже в избранном',
            error_not_exists_message='Рецепт не в избранном',
            serializer_class=RecipeMinifiedSerializer
        )

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def shopping_cart(self, request, pk=None):

        return self.handle_collection_action(
            request=request,
            pk=pk,
            model_class=ShoppingCart,
            success_message='Рецепт успешно добавлен в список покупок',
            error_exists_message='Рецепт уже в списке покупок',
            error_not_exists_message='Рецепт не в списке покупок',
            serializer_class=RecipeMinifiedSerializer
        )

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        user = request.user

        cart_recipes = Recipe.objects.filter(
            in_shopping_cart__user=user
        ).prefetch_related(
            Prefetch(
                'recipe_ingredients',
                queryset=RecipeIngredient.objects.select_related('ingredient')
            )
        )

        ingredients_dict = {}

        for recipe in cart_recipes:
            for recipe_ingredient in recipe.recipe_ingredients.all():
                ingredient = recipe_ingredient.ingredient
                key = (ingredient.name, ingredient.measurement_unit)

                if key in ingredients_dict:
                    ingredients_dict[key] += recipe_ingredient.amount
                else:
                    ingredients_dict[key] = recipe_ingredient.amount

        sorted_ingredients = sorted(ingredients_dict.items(),
                                    key=lambda x: x[0][0])

        shopping_list = [
            f"Список покупок для {user.first_name} {user.last_name}\n\n"
        ]

        for (name, unit), amount in sorted_ingredients:
            shopping_list.append(
                f"{name} ({unit}) — {amount}\n"
            )

        response = HttpResponse(
            content='\n'.join(shopping_list),
            content_type='text/plain'
        )
        response[
            'Content-Disposition'] = 'attachment; filename="shopping_list.txt"'
        return response

    @action(
        detail=True,
        methods=['get'],
        url_path='get-link'
    )
    def get_link(self, request, pk=None):
        recipe = get_object_or_404(Recipe, id=pk)
        serializer = RecipeGetShortLinkSerializer(
            recipe, context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

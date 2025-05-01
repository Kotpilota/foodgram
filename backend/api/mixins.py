from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from recipes.models import Recipe
from users.models import User


class CollectionActionMixin:
    """Миксин для действий с коллекциями рецептов."""

    def handle_favorite_action(
            self, request, pk, model_class, serializer_class):
        """Обрабатывает действия добавления/удаления рецептов в избранное."""
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)

        if request.method == 'POST':
            if model_class.objects.filter(user=user, recipe=recipe).exists():
                return Response(
                    {'error': 'Рецепт уже в избранном'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            data = {'user': user.id, 'recipe': recipe.id}
            serializer = serializer_class(
                data=data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        elif request.method == 'DELETE':
            deleted, _ = model_class.objects.filter(
                user=user, recipe=recipe).delete()
            if not deleted:
                return Response(
                    {'error': 'Рецепт не в избранном'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            return Response(status=status.HTTP_204_NO_CONTENT)

    def handle_shopping_cart_action(
            self, request, pk, model_class, serializer_class):
        """Обрабатывает действия добавления/удаления рецептов в список."""
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)

        if request.method == 'POST':
            if model_class.objects.filter(user=user, recipe=recipe).exists():
                return Response(
                    {'error': 'Рецепт уже в списке покупок'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            data = {'user': user.id, 'recipe': recipe.id}
            serializer = serializer_class(
                data=data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        elif request.method == 'DELETE':
            deleted, _ = model_class.objects.filter(
                user=user, recipe=recipe).delete()
            if not deleted:
                return Response(
                    {'error': 'Рецепт не в списке покупок'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            return Response(status=status.HTTP_204_NO_CONTENT)


class SubscriptionActionMixin:
    """Миксин для действий с подписками на авторов."""

    def handle_subscription_action(
            self, request, user_id, model_class, serializer_class):
        """Обрабатывает действия подписки/отписки от авторов."""
        user = request.user
        author = get_object_or_404(User, id=user_id)

        if request.method == 'POST':
            if user == author:
                return Response(
                    {'error': 'Нельзя подписаться на самого себя'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if model_class.objects.filter(user=user, author=author).exists():
                return Response(
                    {'error': 'Вы уже подписаны на этого автора'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            data = {'user': user.id, 'author': author.id}
            serializer = serializer_class(
                data=data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        elif request.method == 'DELETE':
            deleted, _ = model_class.objects.filter(
                user=user, author=author).delete()
            if not deleted:
                return Response(
                    {'error': 'Вы не подписаны на этого автора'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            return Response(status=status.HTTP_204_NO_CONTENT)

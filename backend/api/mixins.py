from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from recipes.models import Recipe
from users.models import User


class CollectionActionMixin:
    """
    Миксин для действий с коллекциями.
    Предоставляет базовую логику добавления/удаления объектов из коллекций.
    """

    def handle_collection_action(self, request, pk, model_class,
                                 success_message,
                                 error_exists_message,
                                 error_not_exists_message,
                                 serializer_class):
        """
        Обрабатывает действия добавления/удаления объектов из коллекций.

        Args:
            request: Объект запроса
            pk: Идентификатор рецепта
            model_class: Класс модели коллекции (Favorite, ShoppingCart)
            success_message: Сообщение об успешном выполнении для POST-запроса
            error_exists_message: Сообщение об ошибке, если объект уже есть
            error_not_exists_message: Сообщение об ошибке, если объекта нет
            serializer_class: Класс сериализатора для возврата данных
        """
        recipe = get_object_or_404(Recipe, id=pk)
        user = request.user

        if request.method == 'POST':
            if model_class.objects.filter(user=user, recipe=recipe).exists():
                return Response(
                    {'error': error_exists_message},
                    status=status.HTTP_400_BAD_REQUEST
                )

            model_class.objects.create(user=user, recipe=recipe)
            serializer = serializer_class(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            collection_item = model_class.objects.filter(user=user,
                                                         recipe=recipe)
            if not collection_item.exists():
                return Response(
                    {'error': error_not_exists_message},
                    status=status.HTTP_400_BAD_REQUEST
                )

            collection_item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class SubscriptionActionMixin:
    """
    Миксин для действий с подписками на авторов.и.
    Предоставляет базовую логику подписки/отписк
    """

    def handle_subscription_action(self, request, user_id, model_class,
                                   serializer_class):
        """
        Обрабатывает действия подписки/отписки от автора.

        Args:
            request: Объект запроса
            user_id: Идентификатор автора
            model_class: Класс модели подписок (Subscription)
            serializer_class: Класс сериализатора для возврата данных
        """
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

            model_class.objects.create(user=user, author=author)
            serializer = serializer_class(
                author, context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            subscription = model_class.objects.filter(
                user=user, author=author
            )
            if not subscription.exists():
                return Response(
                    {'error': 'Вы не подписаны на этого автора'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from recipes.models import Recipe
from users.models import User


class BaseCollectionMixin:
    """Базовый миксин для действий с коллекциями и подписками."""

    def handle_collection_action(self, request, obj_id, model_class,
                                 success_message=None,
                                 error_exists_message=None,
                                 error_not_exists_message=None,
                                 serializer_class=None,
                                 obj_model=None,
                                 obj_field_name='recipe',
                                 author_field_name=None):
        """Обрабатывает действия добавления/удаления объектов из коллекций."""
        user = request.user

        if request.method == 'POST':
            obj = get_object_or_404(obj_model or Recipe, id=obj_id)
            filter_params = {'user': user}

            if author_field_name:
                filter_params[author_field_name] = obj
            else:
                filter_params[obj_field_name] = obj

            if model_class.objects.filter(**filter_params).exists():
                return Response(
                    {'error': error_exists_message},
                    status=status.HTTP_400_BAD_REQUEST
                )

            instance = model_class(**filter_params)
            instance.save()

            serializer = serializer_class(
                obj, context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        elif request.method == 'DELETE':
            filter_params = {'user': user}
            if author_field_name:
                filter_params[author_field_name] = obj_id
            else:
                filter_params[obj_field_name + '_id'] = obj_id
            deleted_count = model_class.objects.filter(
                **filter_params).delete()[0]
            if not deleted_count:
                return Response(
                    {'error': error_not_exists_message},
                    status=status.HTTP_400_BAD_REQUEST
                )

            return Response(status=status.HTTP_204_NO_CONTENT)


class CollectionActionMixin(BaseCollectionMixin):
    """Миксин для действий с коллекциями рецептов."""

    def handle_collection_action(self, request, pk, model_class,
                                 success_message,
                                 error_exists_message,
                                 error_not_exists_message,
                                 serializer_class):
        """Обрабатывает действия с рецептами в коллекциях."""
        return super().handle_collection_action(
            request=request,
            obj_id=pk,
            model_class=model_class,
            error_exists_message=error_exists_message,
            error_not_exists_message=error_not_exists_message,
            serializer_class=serializer_class,
            obj_model=Recipe,
            obj_field_name='recipe'
        )


class SubscriptionActionMixin(BaseCollectionMixin):
    """Миксин для действий с подписками на авторов."""

    def handle_subscription_action(self, request, user_id, model_class,
                                   serializer_class):
        """Обрабатывает действия подписки/отписки от авторов."""
        if request.method == 'POST':
            author = get_object_or_404(User, id=user_id)
            if request.user == author:
                return Response(
                    {'error': 'Нельзя подписаться на самого себя'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        return super().handle_collection_action(
            request=request,
            obj_id=user_id,
            model_class=model_class,
            error_exists_message='Вы уже подписаны на этого автора',
            error_not_exists_message='Вы не подписаны на этого автора',
            serializer_class=serializer_class,
            obj_model=User,
            obj_field_name='author',
            author_field_name='author'
        )

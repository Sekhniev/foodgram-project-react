from api.serializers import (CustomUserSerializer, SubscribeSerializer,
                             UserListSerializer)
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.db.models.expressions import Exists, OuterRef, Value
from djoser.views import UserViewSet
from recipes.models import Subscribe
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

User = get_user_model()


class UserViewSet(UserViewSet):
    serializer_class = CustomUserSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return User.objects.annotate(
            is_subscribed=Exists(
                self.request.user.follower.filter(
                    author=OuterRef('id'))
            )).prefetch_related(
                'follower', 'following'
        ) if self.request.user.is_authenticated else User.objects.annotate(
            is_subscribed=Value(False))

    def get_serializer_class(self):
        if self.request.method.lower() == 'post':
            return CustomUserSerializer
        return UserListSerializer

    def perform_create(self, serializer):
        password = make_password(self.request.data['password'])
        serializer.save(password=password)

    @action(
        detail=False,
        permission_classes=(IsAuthenticated,))
    def subscriptions(self, request):
        user = request.user
        queryset = Subscribe.objects.filter(user=user)
        pages = self.paginate_queryset(queryset)
        serializer = SubscribeSerializer(
            pages, many=True,
            context={'request': request})
        return self.get_paginated_response(serializer.data)

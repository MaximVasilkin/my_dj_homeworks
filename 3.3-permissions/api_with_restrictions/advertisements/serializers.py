from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from advertisements.models import Advertisement


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', )
        read_only_fields = ['creator']


    def create(self, validated_data):
        """Метод для создания"""
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)



    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""
        req = self.context['request']
        creator = req.user
        http_method = req.method
        open_status = 'OPEN'
        limit = 10
        count_opened_advs = Advertisement.objects.filter(creator=creator, status=open_status).count()
        data_status = data.get('status', '')
        if (http_method == 'POST' or http_method == 'PATCH' and data_status == open_status) and count_opened_advs >= limit:
            raise ValidationError(f'Нельзя иметь более {limit} открытых объявлений')
        return data

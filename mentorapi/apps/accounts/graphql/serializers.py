from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from djoser.serializers import UidAndTokenSerializer, PasswordRetypeSerializer
from djoser import utils
from rest_framework import serializers

from .models import Profile, Company

User = get_user_model()


class UidAndTokenSerializer(UidAndTokenSerializer):

    def validate_uid(self, value):
        try:
            uid = utils.decode_uid(value)
            self.user = User.objects.get(pk=uid)
        except (
                User.DoesNotExist,
                ValueError,
                TypeError,
                OverflowError
        ) as error:
            raise serializers.ValidationError(
                self.error_messages['invalid_uid'])
        return value

    def validate(self, attrs):
        self.validate_uid(attrs['uid'])
        if not default_token_generator.check_token(self.user, attrs['token']):
            raise serializers.ValidationError(
                self.error_messages['invalid_token'])
        return attrs


class PasswordResetConfirmRetypeSerializer(
        UidAndTokenSerializer, PasswordRetypeSerializer
):
    def validate(self, attrs):
        attrs = super(PasswordResetConfirmRetypeSerializer, self)\
            .validate(attrs)
        if attrs['new_password'] != attrs['re_new_password']:
            raise serializers.ValidationError(
                self.error_messages['password_mismatch'])
        return attrs


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'role', 'is_active', 'password', )

    def create(self, validated_data):
        user = User.objects.create(
                email=validated_data['email'],
                role=validated_data['role'],
                is_active=validated_data['is_active']
                )
        user.set_password(validated_data['password'])
        user.save()
        if (validated_data['role'] == "tyalent" or validated_data['role'] == "agent"):
            Profile.objects.create(user=user)
        else:
            Company.objects.create(user=user)
        return user

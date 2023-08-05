"""
引入rest_framework的serializers方便資料序列化, 方便看
"""
from rest_framework import serializers
from reg.models import UserIfm

class RegisterSerializer(serializers.Serializer):
    """
    用來傳輸用戶註冊、修改個人資訊時所輸入的東西。
    """
    # 使用者輸入
    email = serializers.CharField(max_length=100)
    username = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=256)
    birthday = serializers.DateField()
    # 後端產生
    id = serializers.IntegerField()
    validation_num = serializers.IntegerField()

    def create(self, validated_data):
        return UserIfm.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        第一種更新方式，用來重設密碼。
        """
        instance.password = validated_data.get('password', instance.password)
        instance.validation_num = validated_data.get('validation_Num', instance.validation_num)
        instance.save()
        return instance

    def update1(self, instance, validated_data):
        """
        第二種更新方式，用在app ifm的使用者重設。
        """
        # instance.Email = validated_data.get('Email', instance.Email)
        instance.username = validated_data.get('username', instance.username)
        instance.birthday = validated_data.get('birthday', instance.birthday)
        instance.save()
        return instance


class RegisterValidationSerializer(serializers.Serializer):
    """
    用來傳輸用戶註冊後驗證的狀況。
    """
    email = serializers.CharField(max_length=100)
    validation = serializers.BooleanField()
    validation_num = serializers.IntegerField()

    def create(self, validated_data):
        return UserIfm.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.validation = validated_data.get('validation', instance.validation)
        instance.validation_num = validated_data.get('validation_num', instance.validation_num)
        instance.save()
        return instance
    
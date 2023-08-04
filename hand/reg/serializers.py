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
    Email = serializers.CharField(max_length=100)
    Username = serializers.CharField(max_length=30)
    Password = serializers.CharField(max_length=256)
    Birthday = serializers.DateField()
    # 後端產生
    id = serializers.IntegerField()
    Validation_Num = serializers.IntegerField()

    def create(self, validated_data):
        return UserIfm.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        第一種更新方式，用來重設密碼。
        """
        instance.Password = validated_data.get('Password', instance.Password)
        instance.Validation_Num = validated_data.get('Validation_Num', instance.Validation_Num)
        instance.save()
        return instance

    def update1(self, instance, validated_data):
        """
        第二種更新方式，用在app ifm的使用者重設。
        """
        instance.Email = validated_data.get('Email', instance.Email)
        instance.Username = validated_data.get('Username', instance.Username)
        instance.Birthday = validated_data.get('Birthday', instance.Birthday)
        instance.save()
        return instance


class RegisterValidationSerializer(serializers.Serializer):
    """
    用來傳輸用戶註冊後驗證的狀況。
    """
    Email = serializers.CharField(max_length=100)
    Validation = serializers.BooleanField()
    Validation_Num = serializers.IntegerField()

    def create(self, validated_data):
        return UserIfm.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.Validation = validated_data.get('Validation', instance.Validation)
        instance.Validation_Num = validated_data.get('Validation_Num', instance.Validation_Num)
        instance.save()
        return instance
    
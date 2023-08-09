"""
引入rest_framework的serializers方便資料序列化, 方便看
"""
from rest_framework import serializers
from ifm.models import UserDefIfm
from reg.models import UserIfm

class UserDefIfmSerializer(serializers.Serializer):
    """
    用來傳輸用戶註冊系統自動生成的資料
    """
    # 使用者輸入
    # headimg = serializers.CharField(max_length=100)
    headimg = serializers.ImageField(default='headimage/defaultimage.png')
    describe = serializers.CharField(max_length=256)
    user_id = serializers.IntegerField()
    score = serializers.FloatField()

    def create(self, validated_data):
        # # 因為user_id是fk所做的特別處理，fk(外鍵)在序列器中存入時需要是他對應到的
        # # 那個model的instance(實例)
        user_instance = UserIfm.objects.get(id=validated_data.get('user_id'))
        validated_data['user_id'] = user_instance
        instance = UserDefIfm.objects.create(**validated_data)
        return instance
        # return UserDefIfm.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.headimg = validated_data.get('headimg', instance.headimg)
        instance.describe = validated_data.get('describe', instance.describe)
        instance.save()
        return instance
    
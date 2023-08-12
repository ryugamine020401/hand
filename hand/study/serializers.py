"""
引入rest_framework的serializers方便資料序列化, 方便看
"""
from rest_framework import serializers
from ifm.models import UseWordCard
from reg.models import UserIfm

class UseWordCardSerializer(serializers.Serializer):
    """
    用來傳輸使用者新增字卡的序列器
    """
    # 使用者輸入
    # headimg = serializers.CharField(max_length=100)

    user_id = serializers.IntegerField()
    img = serializers.ImageField()
    word = serializers.CharField(max_length=10)
    upload_date = serializers.DateField(default=False)

    def create(self, validated_data):
        # # 因為user_id是fk所做的特別處理，fk(外鍵)在序列器中存入時需要是他對應到的
        # # 那個model的instance(實例)
        user_instance = UserIfm.objects.get(id=validated_data.get('user_id'))
        validated_data['user_id'] = user_instance
        instance = UseWordCard.objects.create(**validated_data)
        return instance
        # return UserDefIfm.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.word = validated_data.get('word', instance.headimg)
        instance.describe = validated_data.get('describe', instance.describe)
        instance.save()
        return instance

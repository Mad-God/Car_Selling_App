from rest_framework import serializers
from sales.models import CarInfo

class CarInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarInfo
        # fields = "__all__"
        exclude = ("owner", "status", "commission", "id", "created_at")
        # fields = ['id', 'owner', "make", "model_name", "condition", "status", "commission_rate", "price", year]

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        breakpoint()
        validated_data["owner"] = self.context['request'].user
        validated_data["commission"] = validated_data["price"] * (validated_data["commission_rate"] /100)
        return CarInfo.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     """
    #     Update and return an existing `Snippet` instance, given the validated data.
    #     """
    #     instance.title = validated_data.get('title', instance.title)
    #     instance.code = validated_data.get('code', instance.code)
    #     instance.linenos = validated_data.get('linenos', instance.linenos)
    #     instance.language = validated_data.get('language', instance.language)
    #     instance.style = validated_data.get('style', instance.style)
    #     instance.save()
    #     return instance
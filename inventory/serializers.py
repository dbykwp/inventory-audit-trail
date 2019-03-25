from rest_framework import serializers
from inventory.models import Item, Users, Variant

class UsersSerializer(serializers.Serializer):
    name = serializers.CharField()
    email_id = serializers.EmailField()
    phone_number = serializers.CharField()

    def create(self, validated_data):
        user = Users(**validated_data)
        user.save()
        return user

class VariantSerializer(serializers.Serializer):
    class Meta:
        model = Variant

    id = serializers.ReadOnlyField()
    name = serializers.CharField(max_length=200)
    selling_price = serializers.FloatField()
    cost_price = serializers.FloatField()
    item_id = serializers.IntegerField()
    size = serializers.CharField(max_length=25)
    options = serializers.CharField(max_length=25)
    quantity = serializers.IntegerField()
    modified_by_id = serializers.IntegerField()
    created_by_id = serializers.IntegerField()

    def create(self, validated_data):
        variant = Variant(**validated_data)
        variant.save()
        return variant

class ItemSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    brand = serializers.CharField(max_length=200)
    category = serializers.CharField(max_length=200)
    product_code = serializers.IntegerField()
    modified_by_id = serializers.IntegerField()
    created_by_id = serializers.IntegerField()



    def create(self, validated_data):
        item = Item(**validated_data)
        item.save()
        return item
        

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.email)
        instance.brand = validated_data.get('brand', instance.content)
        instance.category = validated_data.get('category', instance.created)
        instance.product_code = validated_data.get('product_code', instance.created)
        instance.save()
        return instance

    def get_json_data(self):
        json_object = self.data
        variants = Variant.objects.filter(item_id=self.instance.product_code)
        json_object['variants'] = VariantSerializer(variants, many=True).data
        return json_object

from rest_framework import serializers
import decimal

from .models import Product, Collection



class ProductSerializer(serializers.ModelSerializer):

    collection = serializers.PrimaryKeyRelatedField(
        queryset=Collection.objects.all()
    )

    class Meta:
        model = Product

        fields = [
            "url",
            "id",
            "tittle",
            "slug",
            "description",
            "price",
            "inventory",
            "collection",
            "owner",
        ]
        read_only_fields = ["owner"]

        extra_kwargs = {
            "inventory": {
                "required": False
            }
        }

def calculate_tax(self, product):
    return product.price * decimal.Decimal(1.1)

'''def create(self, validated_data):
    Product = Product(**validated_data)
    Product.other = 1
    Product.save()
    return Product
   # return super().create(validated_data)

def update(self, instance, validated_data):
    instance.unit_price = validated_data.get('unit_price')
    instance.save()
    return instance

'''
class CollectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Collection

        fields = [
            "id",
            "tittle",
            "featured_product",
        ]



from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField



class MessageSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    name = serializers.CharField(max_length=200, required=True)
    phone = PhoneNumberField(required=True)


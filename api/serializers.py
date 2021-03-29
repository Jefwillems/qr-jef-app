from rest_framework import serializers
from api.models import LinkUrl, QRCode, ApiHit


class LinkUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinkUrl
        fields = '__all__'


class QRCodeSerializer(serializers.ModelSerializer):
    urls = LinkUrlSerializer(many=True, read_only=True)

    class Meta:
        model = QRCode
        fields = '__all__'
        read_only_fields = ['created', 'last_updated']


class ApiHitSerializer(serializers.ModelSerializer):
    code = QRCodeSerializer()

    class Meta:
        model = ApiHit
        fields = '__all__'

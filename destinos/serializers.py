from rest_framework import serializers

from .models import BlogEmpresa, Destino, Garantia, OfertaEmpresa, Paquete, Testimonio

class DestinoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destino
        fields = '__all__'

class PaqueteSerializer(serializers.ModelSerializer):
    destino_nombre = serializers.CharField(source='destino.pais', read_only=True)
    
    class Meta:
        model = Paquete
        fields = '__all__'

class TestimonioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonio
        fields = '__all__'

class GarantiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Garantia
        fields = '__all__'


class OfertaEmpresaSerializer(serializers.ModelSerializer):
    destino_nombre = serializers.CharField(source='destino.pais', read_only=True)

    class Meta:
        model = OfertaEmpresa
        fields = '__all__'
        read_only_fields = ['created_at']


class BlogEmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogEmpresa
        fields = '__all__'
        read_only_fields = ['created_at']

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
    foto_url = serializers.SerializerMethodField()

    class Meta:
        model = Testimonio
        fields = ['id', 'nombre', 'foto', 'foto_url', 'texto', 'viaje', 'rating', 'aprobado', 'fecha']
        read_only_fields = ['id', 'fecha']

    def get_foto_url(self, obj):
        if obj.foto:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.foto.url)
            return obj.foto.url
        return None

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

from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import BlogEmpresa, Destino, Garantia, OfertaEmpresa, Paquete, Testimonio
from .serializers import (
    BlogEmpresaSerializer,
    DestinoSerializer,
    GarantiaSerializer,
    OfertaEmpresaSerializer,
    PaqueteSerializer,
    TestimonioSerializer,
)

class DestinoViewSet(viewsets.ModelViewSet):
    queryset = Destino.objects.filter(activo=True)
    serializer_class = DestinoSerializer
    permission_classes = [AllowAny]

class PaqueteViewSet(viewsets.ModelViewSet):
    queryset = Paquete.objects.filter(disponible=True)
    serializer_class = PaqueteSerializer
    permission_classes = [AllowAny]

class TestimonioViewSet(viewsets.ModelViewSet):
    queryset = Testimonio.objects.filter(aprobado=True)
    serializer_class = TestimonioSerializer
    permission_classes = [AllowAny]

class GarantiaViewSet(viewsets.ModelViewSet):
    queryset = Garantia.objects.filter(activo=True)
    serializer_class = GarantiaSerializer
    permission_classes = [AllowAny]


class OfertaEmpresaViewSet(viewsets.ModelViewSet):
    queryset = OfertaEmpresa.objects.select_related('destino').all()
    serializer_class = OfertaEmpresaSerializer
    permission_classes = [AllowAny]


class BlogEmpresaViewSet(viewsets.ModelViewSet):
    queryset = BlogEmpresa.objects.all()
    serializer_class = BlogEmpresaSerializer
    permission_classes = [AllowAny]

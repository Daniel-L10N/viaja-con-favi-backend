from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Destino, Paquete, Testimonio, Garantia
from .serializers import (
    DestinoSerializer, 
    PaqueteSerializer, 
    TestimonioSerializer, 
    GarantiaSerializer
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
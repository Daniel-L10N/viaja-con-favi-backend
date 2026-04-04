from django.urls import path, include
from rest_framework.routers import DefaultRouter
from leads.views import LeadViewSet
from destinos.views import DestinoViewSet, PaqueteViewSet, TestimonioViewSet, GarantiaViewSet
from membresias.views import PlanViewSet
from .auth_views import login_view

router = DefaultRouter()
router.register(r'leads', LeadViewSet, basename='lead')
router.register(r'destinos', DestinoViewSet, basename='destino')
router.register(r'paquetes', PaqueteViewSet, basename='paquete')
router.register(r'testimonios', TestimonioViewSet, basename='testimonio')
router.register(r'garantias', GarantiaViewSet, basename='garantia')
router.register(r'planes', PlanViewSet, basename='plan')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/login/', login_view, name='login'),
]
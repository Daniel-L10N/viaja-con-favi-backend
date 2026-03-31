from django.db import models
from django.conf import settings


class Plan(models.Model):
    PLAN_CHOICES = [
        ('titanium', 'Titanium'),
        ('vip_platinum', 'VIP Platinum'),
    ]
    
    nombre = models.CharField(max_length=50, choices=PLAN_CHOICES, unique=True)
    subtitulo = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    moneda = models.CharField(max_length=3, default='USD')
    mensualidad = models.DecimalField(max_digits=10, decimal_places=2)
    puntos_inicio = models.IntegerField(default=0)
    puntos_mensuales = models.IntegerField(default=0)
    descripcion = models.TextField()
    caracteristicas = models.JSONField(default=list)
    activo = models.BooleanField(default=True)
    orden = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['orden']
        verbose_name = 'Plan'
        verbose_name_plural = 'Planes'
    
    def __str__(self):
        return f"{self.get_nombre_display()} - ${self.precio}"


class Membresia(models.Model):
    PLAN_CHOICES = [
        ('titanium', 'Titanium'),
        ('vip_platinum', 'VIP Platinum'),
    ]
    
    ESTADO_CHOICES = [
        ('activa', 'Activa'),
        ('cancelada', 'Cancelada'),
        ('suspendida', 'Suspendida'),
        ('pendiente', 'Pendiente de pago'),
    ]
    
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='membresias'
    )
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_renovacion = models.DateField(blank=True, null=True)
    puntos_acumulados = models.IntegerField(default=0)
    puntos_canjeados = models.IntegerField(default=0)
    num_referidos_activos = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Membresía'
        verbose_name_plural = 'Membresías'
    
    def __str__(self):
        return f"{self.usuario.email} - {self.plan}"


class Referral(models.Model):
    referidor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='referidos_dados'
    )
    referido = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='referido_desde'
    )
    membresia = models.ForeignKey(
        Membresia,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='referrals'
    )
    fecha = models.DateTimeField(auto_now_add=True)
    membresia_activa = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-fecha']
        verbose_name = 'Referido'
        verbose_name_plural = 'Referidos'
    
    def __str__(self):
        return f"{self.referidor.email} -> {self.referido.email}"
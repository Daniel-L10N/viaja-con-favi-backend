from django.db import models

class Lead(models.Model):
    PLAN_CHOICES = [
        ('titanium', 'Titanium'),
        ('vip_platinum', 'VIP Platinum'),
        ('informacion', 'Solo información'),
    ]
    
    ESTADO_CHOICES = [
        ('nuevo', 'Nuevo'),
        ('contactado', 'Contactado'),
        ('convertido', 'Convertido'),
        ('perdido', 'Perdido'),
    ]
    
    nombre = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=50)
    mensaje = models.TextField(blank=True, null=True)
    plan_interes = models.CharField(max_length=20, choices=PLAN_CHOICES, default='informacion')
    origen = models.CharField(max_length=50, default='viaja-con-favi')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='nuevo')
    notas = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Lead'
        verbose_name_plural = 'Leads'
    
    def __str__(self):
        return f"{self.nombre} - {self.email}"

from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    telefono = models.CharField(max_length=50, blank=True, null=True)
    pais = models.CharField(max_length=100, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    referido_por = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='referidos'
    )
    codigo_referido = models.CharField(max_length=20, unique=True, blank=True, null=True)
    puntos_disponibles = models.IntegerField(default=0)
    foto_perfil = models.URLField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
    
    def __str__(self):
        return f"{self.get_full_name() or self.username} - {self.email}"
    
    def save(self, *args, **kwargs):
        if not self.codigo_referido:
            import uuid
            self.codigo_referido = f"VF{str(uuid.uuid4())[:8].upper()}"
        super().save(*args, **kwargs)
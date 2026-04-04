from django.db import models

class Destino(models.Model):
    CONTINENTE_CHOICES = [
        ('america_norte', 'América del Norte'),
        ('america_central', 'América Central'),
        ('america_sur', 'América del Sur'),
        ('europa', 'Europa'),
        ('asia', 'Asia'),
        ('africa', 'Africa'),
        ('oceania', 'Oceanía'),
    ]
    
    pais = models.CharField(max_length=100)
    codigo_pais = models.CharField(max_length=3)
    bandera_emoji = models.CharField(max_length=10)
    imagen = models.URLField()
    numero_resorts = models.IntegerField()
    continente = models.CharField(max_length=20, choices=CONTINENTE_CHOICES)
    comida = models.CharField(max_length=100)
    transfers = models.CharField(max_length=100)
    extras = models.JSONField(default=list)
    precio_desde = models.CharField(max_length=20)
    descripcion = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    orden = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['orden', 'pais']
        verbose_name = 'Destino'
        verbose_name_plural = 'Destinos'
    
    def __str__(self):
        return f"{self.bandera_emoji} {self.pais}"


class Paquete(models.Model):
    destino = models.ForeignKey(
        Destino, 
        on_delete=models.CASCADE,
        related_name='paquetes'
    )
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    duracion_dias = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    moneda = models.CharField(max_length=3, default='USD')
    incluye = models.JSONField(default=list)
    imagen = models.URLField(blank=True, null=True)
    disponible = models.BooleanField(default=True)
    destacado = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-destacado', 'precio']
        verbose_name = 'Paquete'
        verbose_name_plural = 'Paquetes'
    
    def __str__(self):
        return f"{self.titulo} - {self.destino.pais}"


class Testimonio(models.Model):
    nombre = models.CharField(max_length=255)
    foto = models.URLField(blank=True, null=True)
    texto = models.TextField()
    viaje = models.CharField(max_length=255)
    rating = models.IntegerField(default=5)
    aprobado = models.BooleanField(default=True)
    fecha = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-fecha']
        verbose_name = 'Testimonio'
        verbose_name_plural = 'Testimonios'
    
    def __str__(self):
        return f"{self.nombre} - {self.viaje}"


class Garantia(models.Model):
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    icono = models.CharField(max_length=50)
    orden = models.IntegerField(default=0)
    activo = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['orden']
        verbose_name = 'Garantía'
        verbose_name_plural = 'Garantías'
    
    def __str__(self):
        return self.titulo


class OfertaEmpresa(models.Model):
    STATUS_CHOICES = [
        ('borrador', 'Borrador'),
        ('publicada', 'Publicada'),
        ('archivada', 'Archivada'),
    ]

    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='ofertas/', blank=True, null=True)
    destino = models.ForeignKey(
        Destino,
        on_delete=models.CASCADE,
        related_name='ofertas_empresa',
    )
    incluye = models.JSONField(default=list)
    duracion = models.CharField(max_length=100)
    destacada = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='borrador')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-destacada', '-created_at']
        verbose_name = 'Oferta empresa'
        verbose_name_plural = 'Ofertas empresa'

    def __str__(self):
        return f"{self.titulo} - {self.destino.pais}"


class BlogEmpresa(models.Model):
    STATUS_CHOICES = [
        ('borrador', 'Borrador'),
        ('publicada', 'Publicada'),
        ('archivada', 'Archivada'),
    ]

    titulo = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    excerpt = models.TextField()
    contenido = models.TextField()
    imagen = models.ImageField(upload_to='blog/', blank=True, null=True)
    autor = models.CharField(max_length=255)
    tags = models.JSONField(default=list)
    lectura_minutos = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='borrador')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Blog empresa'
        verbose_name_plural = 'Blog empresa'

    def __str__(self):
        return self.titulo

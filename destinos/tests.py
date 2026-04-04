from decimal import Decimal

from django.db import IntegrityError, transaction
from django.test import TestCase

from .models import BlogEmpresa, Destino, OfertaEmpresa, Paquete


class DestinoModelTests(TestCase):
    def test_crear_destino(self):
        destino = Destino.objects.create(
            pais='Mexico',
            codigo_pais='MEX',
            bandera_emoji='🇲🇽',
            imagen='https://example.com/mexico.jpg',
            numero_resorts=12,
            continente='america_norte',
            comida='Todo incluido',
            transfers='Aeropuerto - hotel',
            extras=['Spa', 'Tours'],
            precio_desde='$499',
            descripcion='Destino de playa',
        )

        self.assertEqual(Destino.objects.count(), 1)
        self.assertEqual(destino.pais, 'Mexico')
        self.assertEqual(destino.continente, 'america_norte')
        self.assertEqual(destino.extras, ['Spa', 'Tours'])

    def test_destino_str(self):
        destino = Destino.objects.create(
            pais='Colombia',
            codigo_pais='COL',
            bandera_emoji='🇨🇴',
            imagen='https://example.com/colombia.jpg',
            numero_resorts=8,
            continente='america_sur',
            comida='Buffet',
            transfers='Incluidos',
            extras=[],
            precio_desde='$399',
        )

        self.assertEqual(str(destino), '🇨🇴 Colombia')

    def test_destino_choices(self):
        self.assertEqual(
            Destino.CONTINENTE_CHOICES,
            [
                ('america_norte', 'América del Norte'),
                ('america_central', 'América Central'),
                ('america_sur', 'América del Sur'),
                ('europa', 'Europa'),
                ('asia', 'Asia'),
                ('africa', 'Africa'),
                ('oceania', 'Oceanía'),
            ],
        )


class PaqueteModelTests(TestCase):
    def setUp(self):
        self.destino = Destino.objects.create(
            pais='Japon',
            codigo_pais='JPN',
            bandera_emoji='🇯🇵',
            imagen='https://example.com/japon.jpg',
            numero_resorts=5,
            continente='asia',
            comida='Desayuno',
            transfers='Opcionales',
            extras=['Guia'],
            precio_desde='$999',
        )

    def test_crear_paquete(self):
        paquete = Paquete.objects.create(
            destino=self.destino,
            titulo='Tokyo Escape',
            descripcion='Paquete de 5 dias',
            duracion_dias=5,
            precio=Decimal('1499.99'),
            moneda='USD',
            incluye=['Hotel', 'Desayuno'],
            imagen='https://example.com/tokyo.jpg',
            destacado=True,
        )

        self.assertEqual(Paquete.objects.count(), 1)
        self.assertEqual(paquete.destino, self.destino)
        self.assertEqual(paquete.precio, Decimal('1499.99'))
        self.assertTrue(paquete.destacado)

    def test_paquete_str(self):
        paquete = Paquete.objects.create(
            destino=self.destino,
            titulo='Kyoto Clasico',
            descripcion='Paquete cultural',
            duracion_dias=4,
            precio=Decimal('999.00'),
            incluye=['Hotel'],
        )

        self.assertEqual(str(paquete), 'Kyoto Clasico - Japon')

    def test_paquete_incluye_json(self):
        incluye = ['Vuelos', 'Hospedaje', {'tipo': 'tour', 'incluido': True}]
        paquete = Paquete.objects.create(
            destino=self.destino,
            titulo='Osaka Experience',
            descripcion='Paquete urbano',
            duracion_dias=6,
            precio=Decimal('1299.50'),
            incluye=incluye,
        )

        paquete.refresh_from_db()

        self.assertEqual(paquete.incluye, incluye)


class OfertaEmpresaModelTests(TestCase):
    def setUp(self):
        self.destino = Destino.objects.create(
            pais='Cancun',
            codigo_pais='MEX',
            bandera_emoji='🇲🇽',
            imagen='https://example.com/cancun.jpg',
            numero_resorts=15,
            continente='america_norte',
            comida='Todo incluido',
            transfers='Incluidos',
            extras=['Spa'],
            precio_desde='$899',
        )

    def test_crear_oferta_empresa(self):
        oferta = OfertaEmpresa.objects.create(
            titulo='Oferta Caribe',
            descripcion='Paquete todo incluido',
            precio=Decimal('1999.99'),
            destino=self.destino,
            incluye=['vuelo', 'hotel'],
            duracion='5 dias',
        )

        self.assertEqual(OfertaEmpresa.objects.count(), 1)
        self.assertEqual(oferta.titulo, 'Oferta Caribe')
        self.assertEqual(oferta.precio, Decimal('1999.99'))
        self.assertEqual(oferta.destino, self.destino)
        self.assertEqual(oferta.status, 'borrador')

    def test_oferta_empresa_incluye_json(self):
        incluye = ['vuelo', 'hotel', {'traslado': True}]
        oferta = OfertaEmpresa.objects.create(
            titulo='Oferta Caribe',
            descripcion='Paquete todo incluido',
            precio=Decimal('1999.99'),
            destino=self.destino,
            incluye=incluye,
            duracion='5 dias',
        )

        self.assertEqual(oferta.incluye, incluye)


class BlogEmpresaModelTests(TestCase):
    def test_crear_blog_empresa(self):
        blog = BlogEmpresa.objects.create(
            titulo='Guia para viajar a Oaxaca',
            slug='guia-para-viajar-a-oaxaca',
            excerpt='Consejos rapidos para tu viaje.',
            contenido='Contenido completo del articulo.',
            autor='Equipo Favi',
            tags=['oaxaca', 'consejos'],
            lectura_minutos=6,
        )

        self.assertEqual(BlogEmpresa.objects.count(), 1)
        self.assertEqual(blog.titulo, 'Guia para viajar a Oaxaca')
        self.assertEqual(blog.slug, 'guia-para-viajar-a-oaxaca')
        self.assertEqual(blog.status, 'borrador')

    def test_blog_empresa_slug_unique(self):
        BlogEmpresa.objects.create(
            titulo='Guia para viajar a Oaxaca',
            slug='guia-para-viajar-a-oaxaca',
            excerpt='Consejos rapidos para tu viaje.',
            contenido='Contenido completo del articulo.',
            autor='Equipo Favi',
            tags=['oaxaca'],
            lectura_minutos=6,
        )

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                BlogEmpresa.objects.create(
                    titulo='Otra guia',
                    slug='guia-para-viajar-a-oaxaca',
                    excerpt='Otro extracto.',
                    contenido='Otro contenido.',
                    autor='Equipo Favi',
                    tags=['mexico'],
                    lectura_minutos=4,
                )

    def test_blog_empresa_tags_json(self):
        tags = ['tips', 'playa', {'temporada': 'verano'}]
        blog = BlogEmpresa.objects.create(
            titulo='Guia de playas',
            slug='guia-de-playas',
            excerpt='Las mejores playas para tus vacaciones.',
            contenido='Contenido completo de playas.',
            autor='Equipo Favi',
            tags=tags,
            lectura_minutos=8,
        )

        self.assertEqual(blog.tags, tags)

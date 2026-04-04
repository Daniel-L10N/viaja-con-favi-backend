from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import Membresia, Plan


class PlanModelTests(TestCase):
    def test_crear_plan(self):
        plan = Plan.objects.create(
            nombre='titanium',
            subtitulo='Plan Titanium',
            precio=Decimal('199.99'),
            moneda='USD',
            mensualidad=Decimal('19.99'),
            puntos_inicio=100,
            puntos_mensuales=25,
            descripcion='Plan base para pruebas',
            caracteristicas=['beneficio 1', 'beneficio 2'],
            activo=True,
            orden=1,
        )

        self.assertEqual(Plan.objects.count(), 1)
        self.assertEqual(plan.nombre, 'titanium')
        self.assertEqual(plan.subtitulo, 'Plan Titanium')
        self.assertEqual(plan.precio, Decimal('199.99'))
        self.assertEqual(plan.caracteristicas, ['beneficio 1', 'beneficio 2'])
        self.assertTrue(plan.activo)

    def test_plan_str(self):
        plan = Plan.objects.create(
            nombre='vip_platinum',
            subtitulo='Plan VIP',
            precio=Decimal('299.00'),
            moneda='USD',
            mensualidad=Decimal('29.00'),
            puntos_inicio=200,
            puntos_mensuales=50,
            descripcion='Plan premium',
            caracteristicas=['acceso preferencial'],
            orden=2,
        )

        self.assertEqual(str(plan), 'VIP Platinum - $299.00')

    def test_plan_tipo_choices(self):
        expected_choices = [
            ('titanium', 'Titanium'),
            ('vip_platinum', 'VIP Platinum'),
        ]

        self.assertEqual(Plan._meta.get_field('nombre').choices, expected_choices)


class MembresiaModelTests(TestCase):
    def setUp(self):
        self.usuario = get_user_model().objects.create_user(
            username='usuario_prueba',
            email='usuario@example.com',
            password='testpass123',
            first_name='Usuario',
            last_name='Prueba',
        )
        self.plan = Plan.objects.create(
            nombre='titanium',
            subtitulo='Plan Titanium',
            precio=Decimal('199.99'),
            moneda='USD',
            mensualidad=Decimal('19.99'),
            puntos_inicio=100,
            puntos_mensuales=25,
            descripcion='Plan base para pruebas',
            caracteristicas=['beneficio 1'],
            orden=1,
        )

    def test_crear_membresia(self):
        membresia = Membresia.objects.create(
            usuario=self.usuario,
            plan=self.plan,
            estado='activa',
            puntos_acumulados=150,
            puntos_canjeados=30,
            num_referidos_activos=2,
        )

        self.assertEqual(Membresia.objects.count(), 1)
        self.assertEqual(membresia.usuario, self.usuario)
        self.assertEqual(membresia.plan, self.plan)
        self.assertEqual(membresia.estado, 'activa')
        self.assertEqual(membresia.puntos_acumulados, 150)

    def test_membresia_str(self):
        membresia = Membresia.objects.create(
            usuario=self.usuario,
            plan=self.plan,
            estado='pendiente',
        )

        self.assertEqual(str(membresia), 'usuario@example.com - Titanium - $199.99')

    def test_membresia_estado_choices(self):
        expected_choices = [
            ('activa', 'Activa'),
            ('cancelada', 'Cancelada'),
            ('suspendida', 'Suspendida'),
            ('pendiente', 'Pendiente de pago'),
        ]

        self.assertEqual(Membresia._meta.get_field('estado').choices, expected_choices)

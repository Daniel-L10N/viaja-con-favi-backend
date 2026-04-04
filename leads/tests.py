from django.db import IntegrityError
from django.test import TestCase

from .models import Lead


class LeadModelTests(TestCase):
    def test_crear_lead(self):
        lead = Lead.objects.create(
            nombre='Ana Perez',
            email='ana@example.com',
            telefono='5551234567',
            mensaje='Quiero informacion',
            plan_interes='titanium',
            origen='landing',
            estado='nuevo',
        )

        self.assertEqual(Lead.objects.count(), 1)
        self.assertEqual(lead.nombre, 'Ana Perez')
        self.assertEqual(lead.plan_interes, 'titanium')
        self.assertEqual(lead.estado, 'nuevo')

    def test_lead_str(self):
        lead = Lead.objects.create(
            nombre='Luis Gomez',
            email='luis@example.com',
            telefono='5559876543',
        )

        self.assertEqual(str(lead), 'Luis Gomez - luis@example.com')

    def test_lead_status_choices(self):
        self.assertEqual(
            Lead.ESTADO_CHOICES,
            [
                ('nuevo', 'Nuevo'),
                ('contactado', 'Contactado'),
                ('convertido', 'Convertido'),
                ('perdido', 'Perdido'),
            ],
        )

    def test_lead_email_unique(self):
        Lead.objects.create(
            nombre='Maria Lopez',
            email='maria@example.com',
            telefono='5551112233',
        )

        with self.assertRaises(IntegrityError):
            Lead.objects.create(
                nombre='Maria Duplicada',
                email='maria@example.com',
                telefono='5554445566',
            )

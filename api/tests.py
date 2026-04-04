from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from destinos.models import BlogEmpresa, Destino, OfertaEmpresa
from leads.models import Lead


class ApiTests(APITestCase):
    def setUp(self):
        self.destino = Destino.objects.create(
            pais="Mexico",
            codigo_pais="MEX",
            bandera_emoji="🇲🇽",
            imagen="https://example.com/mexico.jpg",
            numero_resorts=12,
            continente="america_norte",
            comida="Tacos",
            transfers="Incluidos",
            extras=["spa", "tour"],
            precio_desde="$999",
            descripcion="Destino activo",
            activo=True,
            orden=1,
        )

    def test_api_ofertas_crud(self):
        create_payload = {
            "titulo": "Escapada a Cancun",
            "descripcion": "Hotel y vuelos incluidos",
            "precio": "1999.99",
            "destino": self.destino.id,
            "incluye": ["vuelo", "hotel", "traslados"],
            "duracion": "5 dias / 4 noches",
            "destacada": True,
            "status": "publicada",
        }

        create_response = self.client.post(reverse("oferta-list"), create_payload, format="json")

        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        oferta_id = create_response.data["id"]
        self.assertTrue(OfertaEmpresa.objects.filter(id=oferta_id).exists())
        self.assertEqual(create_response.data["destino_nombre"], self.destino.pais)

        list_response = self.client.get(reverse("oferta-list"))

        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(list_response.data), 1)
        self.assertEqual(list_response.data[0]["titulo"], create_payload["titulo"])

        detail_url = reverse("oferta-detail", args=[oferta_id])
        update_payload = {
            **create_payload,
            "titulo": "Escapada a Riviera Maya",
            "precio": "2199.50",
            "destacada": False,
        }

        update_response = self.client.put(detail_url, update_payload, format="json")

        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(update_response.data["titulo"], update_payload["titulo"])

        delete_response = self.client.delete(detail_url)

        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(OfertaEmpresa.objects.filter(id=oferta_id).exists())

    def test_api_blog_crud(self):
        create_payload = {
            "titulo": "Guia para viajar mejor",
            "slug": "guia-para-viajar-mejor",
            "excerpt": "Consejos practicos para tu proximo viaje",
            "contenido": "Contenido largo del articulo",
            "autor": "Equipo Favi",
            "tags": ["tips", "viajes"],
            "lectura_minutos": 6,
            "status": "publicada",
        }

        create_response = self.client.post(reverse("blog-list"), create_payload, format="json")

        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        blog_id = create_response.data["id"]
        self.assertTrue(BlogEmpresa.objects.filter(id=blog_id).exists())

        list_response = self.client.get(reverse("blog-list"))

        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(list_response.data), 1)
        self.assertEqual(list_response.data[0]["slug"], create_payload["slug"])

        detail_url = reverse("blog-detail", args=[blog_id])
        update_payload = {
            **create_payload,
            "titulo": "Guia actualizada para viajar mejor",
            "slug": "guia-actualizada-para-viajar-mejor",
            "lectura_minutos": 8,
        }

        update_response = self.client.put(detail_url, update_payload, format="json")

        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(update_response.data["titulo"], update_payload["titulo"])

        delete_response = self.client.delete(detail_url)

        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(BlogEmpresa.objects.filter(id=blog_id).exists())

    def test_api_leads_create(self):
        payload = {
            "nombre": "Daniel Soto",
            "email": "daniel@example.com",
            "telefono": "5552223333",
            "mensaje": "Quiero informacion del plan VIP",
            "plan_interes": "vip_platinum",
            "notas": "Contactar por la tarde",
        }

        response = self.client.post(reverse("lead-list"), payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["mensaje"], "Lead creado exitosamente")
        self.assertIn("id", response.data)

        lead = Lead.objects.get(id=response.data["id"])
        self.assertEqual(lead.nombre, payload["nombre"])
        self.assertEqual(lead.origen, "viaja-con-favi")
        self.assertEqual(lead.estado, "nuevo")

    def test_api_destinos_list(self):
        Destino.objects.create(
            pais="Japon",
            codigo_pais="JP",
            bandera_emoji="🇯🇵",
            imagen="https://example.com/japon.jpg",
            numero_resorts=8,
            continente="asia",
            comida="Sushi",
            transfers="Opcionales",
            extras=["guia"],
            precio_desde="$1999",
            descripcion="Destino inactivo",
            activo=False,
            orden=2,
        )

        response = self.client.get(reverse("destino-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.destino.id)
        self.assertEqual(response.data[0]["pais"], "Mexico")

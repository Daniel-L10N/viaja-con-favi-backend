import django.db.models.deletion
from django.db import migrations, models
from django.utils.text import slugify


def _table_exists(connection, table_name):
    with connection.cursor() as cursor:
        tables = connection.introspection.table_names(cursor)
    return table_name in tables


def _build_destino_defaults(nombre):
    slug = slugify(nombre or 'destino')
    codigo = (slug.replace('-', '')[:3] or 'GEN').upper()
    return {
        'pais': nombre or 'Destino general',
        'codigo_pais': codigo,
        'bandera_emoji': '🌍',
        'imagen': 'https://example.com/destino.jpg',
        'numero_resorts': 0,
        'continente': 'america_norte',
        'comida': 'Por definir',
        'transfers': 'Por definir',
        'extras': [],
        'precio_desde': '$0',
        'descripcion': 'Destino migrado desde clientes.',
        'activo': False,
        'orden': 999,
    }


def migrar_clientes_a_destinos(apps, schema_editor):
    connection = schema_editor.connection
    if not _table_exists(connection, 'clientes_publicacionoferta') and not _table_exists(connection, 'clientes_publicacionblog'):
        return

    Destino = apps.get_model('destinos', 'Destino')
    OfertaEmpresa = apps.get_model('destinos', 'OfertaEmpresa')
    BlogEmpresa = apps.get_model('destinos', 'BlogEmpresa')

    if _table_exists(connection, 'clientes_publicacionoferta'):
        with connection.cursor() as cursor:
            cursor.execute(
                '''
                SELECT titulo, descripcion, precio, imagen, destino, incluye, duracion, destacada, status, created_at
                FROM clientes_publicacionoferta
                '''
            )
            for (
                titulo,
                descripcion,
                precio,
                imagen,
                destino_nombre,
                incluye,
                duracion,
                destacada,
                status,
                created_at,
            ) in cursor.fetchall():
                destino = Destino.objects.filter(pais__iexact=destino_nombre).first()
                if destino is None:
                    destino = Destino.objects.create(**_build_destino_defaults(destino_nombre))

                OfertaEmpresa.objects.create(
                    titulo=titulo,
                    descripcion=descripcion,
                    precio=precio,
                    imagen=imagen,
                    destino=destino,
                    incluye=incluye or [],
                    duracion=duracion,
                    destacada=bool(destacada),
                    status=status or 'borrador',
                    created_at=created_at,
                )

    if _table_exists(connection, 'clientes_publicacionblog'):
        with connection.cursor() as cursor:
            cursor.execute(
                '''
                SELECT titulo, slug, excerpt, contenido, imagen, autor, tags, lectura_minutos, status, created_at
                FROM clientes_publicacionblog
                '''
            )
            for (
                titulo,
                slug,
                excerpt,
                contenido,
                imagen,
                autor,
                tags,
                lectura_minutos,
                status,
                created_at,
            ) in cursor.fetchall():
                BlogEmpresa.objects.update_or_create(
                    slug=slug,
                    defaults={
                        'titulo': titulo,
                        'excerpt': excerpt,
                        'contenido': contenido,
                        'imagen': imagen,
                        'autor': autor,
                        'tags': tags or [],
                        'lectura_minutos': lectura_minutos,
                        'status': status or 'borrador',
                        'created_at': created_at,
                    },
                )


class Migration(migrations.Migration):

    dependencies = [
        ('destinos', '0002_garantia_testimonio'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogEmpresa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('excerpt', models.TextField()),
                ('contenido', models.TextField()),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='blog/')),
                ('autor', models.CharField(max_length=255)),
                ('tags', models.JSONField(default=list)),
                ('lectura_minutos', models.PositiveIntegerField()),
                ('status', models.CharField(choices=[('borrador', 'Borrador'), ('publicada', 'Publicada'), ('archivada', 'Archivada')], default='borrador', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Blog empresa',
                'verbose_name_plural': 'Blog empresa',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='OfertaEmpresa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=255)),
                ('descripcion', models.TextField()),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='ofertas/')),
                ('incluye', models.JSONField(default=list)),
                ('duracion', models.CharField(max_length=100)),
                ('destacada', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('borrador', 'Borrador'), ('publicada', 'Publicada'), ('archivada', 'Archivada')], default='borrador', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('destino', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ofertas_empresa', to='destinos.destino')),
            ],
            options={
                'verbose_name': 'Oferta empresa',
                'verbose_name_plural': 'Ofertas empresa',
                'ordering': ['-destacada', '-created_at'],
            },
        ),
        migrations.RunPython(migrar_clientes_a_destinos, migrations.RunPython.noop),
    ]

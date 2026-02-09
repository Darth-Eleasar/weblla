# Generated migration file

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('huella_app', '0002_inepoblacion_inemunicipio_importacionhuella'),
    ]

    operations = [
        migrations.CreateModel(
            name='MenuConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mostrar_huellas', models.BooleanField(default=True, help_text='Mostrar sección de Huellas')),
                ('mostrar_importar', models.BooleanField(default=False, help_text='Mostrar sección de Importar CSV')),
                ('mostrar_reportes', models.BooleanField(default=False, help_text='Mostrar sección de Reportes')),
                ('mostrar_usuarios', models.BooleanField(default=False, help_text='Mostrar gestión de usuarios')),
                ('mostrar_resolucion', models.BooleanField(default=False, help_text='Mostrar resolución de incidencias')),
                ('rol', models.OneToOneField(help_text='Grupo/Rol al que pertenece esta configuración', on_delete=django.db.models.deletion.CASCADE, to='auth.group')),
            ],
            options={
                'verbose_name': 'Configuración de Menú',
                'verbose_name_plural': 'Configuraciones de Menú',
            },
        ),
    ]

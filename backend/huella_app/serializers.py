# Programa: Weblla
# Veersion: 1.1
# Autor: Equipo Weblla
# Fecha: 28-01-2026
# Última Modificación: 02-02-2026
# Cambio realizado: Añadido serializador para gestión de usuarios.
# Descripción:
# Serializadores para la aplicación Huella.

from rest_framework import serializers
from django.contrib.auth.models import User, Group
from .models import Huella, ImportacionHuella, UserProfile, MenuConfig, AuditLog

# =======================================================
# TUS SERIALIZADORES ORIGINALES (INTACTOS)
# =======================================================

class HuellaSerializer(serializers.ModelSerializer):
    """Serializador completo para Huella con todos los campos."""
    
    class Meta:
        model = Huella
        fields = [
            'id',
            'iddomicilioto',
            'codigopostal',
            'provincia',
            'poblacion',
            'tipovia',
            'nombrevia',
            'idtecnicovia',
            'numero',
            'bisduplicado',
            'bloquedelafinca',
            'identificadorfincaportal',
            'letrafinca',
            'escalera',
            'planta',
            'mano1',
            'mano2',
            'observaciones',
            'flagdummy',
            'codigoinevia',
            'codigocensal',
            'codigopai',
            'codigoolt',
            'codigocto',
            'tipocto',
            'direccioncto',
            'tipopermiso',
            'tipocajaderivacion',
            'numunidadesinmobiliarias',
            'numviviendas',
            'fechaalta',
            'codigocajaderivacion',
            'ubicacioncajaderivacion',
            'coinv',
            'area_comercial',
            'lat',
            'lng',
            'created',
            'updated',
        ]
        read_only_fields = ['id', 'created', 'updated']


class HuellaListSerializer(serializers.ModelSerializer):
    """Serializador reducido para listados (mejor rendimiento)."""
    
    class Meta:
        model = Huella
        fields = [
            'id',
            'iddomicilioto',
            'codigopostal',
            'provincia',
            'poblacion',
            'nombrevia',
            'numero',
            'codigoolt',
            'codigocto',
            'created',
        ]

# =======================================================
# LO NUEVO: SERIALIZADOR PARA IMPORTACIONES
# =======================================================

class ImportacionHuellaSerializer(serializers.ModelSerializer):
    # Campo extra para mostrar el nombre del usuario en vez de su ID numérico
    usuario_nombre = serializers.ReadOnlyField(source='usuario.username')

    class Meta:
        model = ImportacionHuella
        fields = '__all__'
        # Estos campos no se pueden editar desde la API, los rellena el sistema
        read_only_fields = ('usuario', 'estado', 'log_proceso', 'fichero_errores', 'fichero_normalizado')


# =======================================================
# SERIALIZADORES PARA AUTENTICACIÓN
# =======================================================

class LoginSerializer(serializers.Serializer):
    """Serializador para login de usuario."""
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        from django.contrib.auth import authenticate
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Usuario o contraseña incorrectos")
        data['user'] = user
        return data


class UserSerializer(serializers.ModelSerializer):
    """Serializador para información del usuario."""
    grupos = serializers.SerializerMethodField()
    permisos = serializers.SerializerMethodField()
    menu = serializers.SerializerMethodField()

    class Meta:
        from django.contrib.auth.models import User
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'grupos', 'permisos', 'is_staff', 'menu']
        read_only_fields = ['id']

    def get_grupos(self, obj):
        """Devuelve los nombres de los grupos del usuario."""
        return list(obj.groups.values_list('name', flat=True))

    def get_permisos(self, obj):
        """Devuelve los permisos del usuario."""
        return list(obj.get_all_permissions())
    
    def get_menu(self, obj):
        """Devuelve la configuración de menú según los grupos del usuario."""
        menu_config = {
            'mostrar_huellas': True,
            'mostrar_importar': False,
            'mostrar_reportes': False,
            'mostrar_usuarios': False,
            'mostrar_resolucion': False,
        }
        
        # Si el usuario tiene grupos, usar la configuración del primer grupo
        if obj.groups.exists():
            try:
                config = MenuConfig.objects.filter(
                    rol__in=obj.groups.all()
                ).first()
                if config:
                    menu_config = {
                        'mostrar_huellas': config.mostrar_huellas,
                        'mostrar_importar': config.mostrar_importar,
                        'mostrar_reportes': config.mostrar_reportes,
                        'mostrar_usuarios': config.mostrar_usuarios,
                        'mostrar_resolucion': config.mostrar_resolucion,
                    }
            except MenuConfig.DoesNotExist:
                pass
        
        return menu_config

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializador para el perfil de usuario."""
    class Meta:
        model = UserProfile
        fields = ['telefono', 'is_active_profile', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class UserManagementSerializer(serializers.ModelSerializer):
    """Serializador completo para gestión de usuarios."""
    grupos = serializers.SerializerMethodField()
    rol = serializers.CharField(write_only=True, required=False)
    telefono = serializers.CharField(source='profile.telefono', required=False, allow_blank=True)
    is_active_profile = serializers.BooleanField(source='profile.is_active_profile', read_only=True)
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'is_active', 'is_staff', 'grupos', 'rol', 'telefono',
            'is_active_profile', 'password', 'date_joined', 'last_login'
        ]
        read_only_fields = ['id', 'date_joined', 'last_login']

    def get_grupos(self, obj):
        return list(obj.groups.values_list('name', flat=True))

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', {})
        rol = validated_data.pop('rol', None)
        password = validated_data.pop('password', None)
        
        # Crear usuario
        user = User.objects.create(**validated_data)
        
        # Establecer contraseña
        if password:
            user.set_password(password)
            user.save()
        
        # Crear o actualizar perfil
        if hasattr(user, 'profile'):
            for key, value in profile_data.items():
                setattr(user.profile, key, value)
            user.profile.save()
        else:
            UserProfile.objects.create(user=user, **profile_data)
        
        # Asignar rol/grupo
        if rol:
            try:
                grupo = Group.objects.get(name=rol)
                user.groups.clear()
                user.groups.add(grupo)
            except Group.DoesNotExist:
                raise serializers.ValidationError({
                    "rol": f"El rol '{rol}' no existe en el sistema."
                })            
        
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        rol = validated_data.pop('rol', None)
        password = validated_data.pop('password', None)
        
        # Actualizar campos del usuario
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # Actualizar contraseña si se proporciona
        if password:
            instance.set_password(password)
        
        instance.save()
        
        # Actualizar perfil
        if profile_data:
            if hasattr(instance, 'profile'):
                for key, value in profile_data.items():
                    setattr(instance.profile, key, value)
                instance.profile.save()
            else:
                UserProfile.objects.create(user=instance, **profile_data)
        
        # Actualizar rol/grupo
        if rol:
            try:
                grupo = Group.objects.get(name=rol)
                instance.groups.clear()
                instance.groups.add(grupo)
            except Group.DoesNotExist:
                pass
        
        return instance


class GroupSerializer(serializers.ModelSerializer):
    """Serializador para grupos/roles."""
    class Meta:
        model = Group
        fields = ['id', 'name']

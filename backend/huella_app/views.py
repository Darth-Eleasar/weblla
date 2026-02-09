# Programa: Weblla
# Veersion: 1.1
# Autor: Equipo Weblla
# Fecha: 28-01-2026
# Última modificación: 02-02-2026
# Cambio realizado: añadido vistas para gestión de usuarios.
# Descripción:
# Vistas para la gestión de huellas y autenticación de usuarios.

from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import Huella, ImportacionHuella
from .serializers import HuellaSerializer, HuellaListSerializer, LoginSerializer, UserSerializer, ImportacionHuellaSerializer
from rest_framework import parsers
from .normalization import normalizar_archivo
from django.contrib.auth.models import User, Group
from .serializers import UserManagementSerializer, GroupSerializer

class HuellaPagination(PageNumberPagination):
    """Paginación personalizada para listados de huellas."""
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 1000

class HuellaViewSet(viewsets.ModelViewSet):
    """
    ViewSet completo para gestionar líneas de huella.
    
    Proporciona:
    - CRUD completo (Create, Read, Update, Delete)
    - Filtrado avanzado
    - Búsqueda por múltiples campos
    - Ordenamiento
    - Acciones personalizadas para búsquedas específicas
    
    Permisos: Requiere autenticación. Los cambios requieren permisos específicos.
    """
    
    queryset = Huella.objects.all()
    serializer_class = HuellaSerializer
    pagination_class = HuellaPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    # Campos disponibles para filtrado
    filterset_fields = [
        'iddomicilioto',
        'codigopostal',
        'provincia',
        'poblacion',
        'tipovia',
        'nombrevia',
        'codigoolt',
        'codigocto',
        'tipocto',
    ]
    
    # Campos disponibles para búsqueda
    search_fields = [
        'iddomicilioto',
        'nombrevia',
        'provincia',
        'poblacion',
        'codigopostal',
        'codigoolt',
        'codigocto',
        'observaciones',
    ]
    
    # Campos disponibles para ordenamiento
    ordering_fields = [
        'created',
        'updated',
        'codigopostal',
        'provincia',
        'poblacion',
        'nombrevia',
    ]
    
    # Orden por defecto
    ordering = ['-created']
    
    def get_serializer_class(self):
        """Usa serializador reducido en listados para mejor rendimiento."""
        if self.action == 'list':
            return HuellaListSerializer
        return HuellaSerializer
    
    @action(detail=False, methods=['get'])
    def por_codigo_postal(self, request):
        """
        Endpoint para obtener huellas filtradas por código postal.
        
        Uso: GET /api/huellas/por_codigo_postal/?codigo=15035
        """
        codigo = request.query_params.get('codigo')
        if not codigo:
            return Response(
                {'error': 'Se requiere parámetro "codigo"'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        huellas = Huella.objects.filter(codigopostal=codigo)
        page = self.paginate_queryset(huellas)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(huellas, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def por_provincia(self, request):
        """
        Endpoint para obtener huellas filtradas por provincia.
        
        Uso: GET /api/huellas/por_provincia/?provincia=A%20CORUÑA
        """
        provincia = request.query_params.get('provincia')
        if not provincia:
            return Response(
                {'error': 'Se requiere parámetro "provincia"'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        huellas = Huella.objects.filter(provincia__icontains=provincia)
        page = self.paginate_queryset(huellas)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(huellas, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def por_poblacion(self, request):
        """
        Endpoint para obtener huellas filtradas por población/municipio.
        
        Uso: GET /api/huellas/por_poblacion/?poblacion=FENE
        """
        poblacion = request.query_params.get('poblacion')
        if not poblacion:
            return Response(
                {'error': 'Se requiere parámetro "poblacion"'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        huellas = Huella.objects.filter(poblacion__icontains=poblacion)
        page = self.paginate_queryset(huellas)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(huellas, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def por_cto(self, request):
        """
        Endpoint para obtener huellas filtradas por CTO.
        
        Uso: GET /api/huellas/por_cto/?codigo=1505432CT0419
        """
        codigo = request.query_params.get('codigo')
        if not codigo:
            return Response(
                {'error': 'Se requiere parámetro "codigo"'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        huellas = Huella.objects.filter(codigocto__icontains=codigo)
        page = self.paginate_queryset(huellas)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(huellas, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def por_olt(self, request):
        """
        Endpoint para obtener huellas filtradas por OLT.
        
        Uso: GET /api/huellas/por_olt/?codigo=RA-15-NARON-02-OLT
        """
        codigo = request.query_params.get('codigo')
        if not codigo:
            return Response(
                {'error': 'Se requiere parámetro "codigo"'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        huellas = Huella.objects.filter(codigoolt__icontains=codigo)
        page = self.paginate_queryset(huellas)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(huellas, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def estadisticas(self, request):
        """
        Endpoint para obtener estadísticas generales.
        
        Uso: GET /api/huellas/estadisticas/
        """
        from django.db.models import Count
        
        total = Huella.objects.count()
        provincias = Huella.objects.values('provincia').distinct().count()
        poblaciones = Huella.objects.values('poblacion').distinct().count()
        codigos_postal = Huella.objects.values('codigopostal').distinct().count()
        
        # Top 5 provincias por cantidad de huellas
        top_provincias = Huella.objects.values('provincia').annotate(
            cantidad=Count('id')
        ).order_by('-cantidad')[:5]
        
        # Top 5 poblaciones por cantidad de huellas
        top_poblaciones = Huella.objects.values('poblacion').annotate(
            cantidad=Count('id')
        ).order_by('-cantidad')[:5]
        
        return Response({
            'total_huellas': total,
            'total_provincias': provincias,
            'total_poblaciones': poblaciones,
            'total_codigos_postal': codigos_postal,
            'top_provincias': list(top_provincias),
            'top_poblaciones': list(top_poblaciones),
        })
    
    @action(detail=True, methods=['get'])
    def vecinos(self, request, pk=None):
        """
        Endpoint para obtener huellas cercanas por dirección.
        
        Uso: GET /api/huellas/{id}/vecinos/
        """
        huella = self.get_object()
        vecinas = Huella.objects.filter(
            nombrevia=huella.nombrevia,
            numero__in=[str(int(huella.numero or 0) - 1), huella.numero, str(int(huella.numero or 0) + 1)],
            poblacion=huella.poblacion
        ).exclude(id=huella.id)
        
        serializer = self.get_serializer(vecinas, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def exportar_csv(self, request):
        """
        Exporta huellas filtradas a CSV descargable.
        
        GET /api/huellas/exportar_csv/?codigopostal=15054&provincia=A%20CORUÑA
        
        Parámetros opcionales:
        - codigopostal
        - provincia
        - poblacion
        - codigoolt
        - codigocto
        """
        import csv
        from io import StringIO
        from django.http import StreamingHttpResponse
        
        # Aplicar filtros
        queryset = Huella.objects.all()
        
        if request.query_params.get('codigopostal'):
            queryset = queryset.filter(codigopostal=request.query_params.get('codigopostal'))
        if request.query_params.get('provincia'):
            queryset = queryset.filter(provincia__icontains=request.query_params.get('provincia'))
        if request.query_params.get('poblacion'):
            queryset = queryset.filter(poblacion__icontains=request.query_params.get('poblacion'))
        if request.query_params.get('codigoolt'):
            queryset = queryset.filter(codigoolt__icontains=request.query_params.get('codigoolt'))
        if request.query_params.get('codigocto'):
            queryset = queryset.filter(codigocto__icontains=request.query_params.get('codigocto'))
        
        # Crear CSV en memoria
        output = StringIO()
        writer = csv.writer(output)
        
        # Escribir encabezados
        campos = [
            'iddomicilioto', 'codigopostal', 'provincia', 'poblacion', 'tipovia', 'nombrevia',
            'numero', 'codigoolt', 'codigocto', 'tipocto', 'observaciones'
        ]
        writer.writerow(campos)
        
        # Escribir datos
        for huella in queryset:
            fila = [
                huella.iddomicilioto,
                huella.codigopostal,
                huella.provincia,
                huella.poblacion,
                huella.tipovia,
                huella.nombrevia,
                huella.numero,
                huella.codigoolt,
                huella.codigocto,
                huella.tipocto,
                huella.observaciones,
            ]
            writer.writerow(fila)
        
        # Crear respuesta descargable
        output.seek(0)
        response = StreamingHttpResponse(output, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="huella_export.csv"'
        
        return response


# =======================================================
# VISTA PARA GESTIONAR IMPORTACIONES DE ARCHIVOS CSV
# =======================================================

class ImportacionViewSet(viewsets.ModelViewSet):
    """
    API para subir ficheros CSV y ver el estado de las importaciones.
    
    Funcionalidades:
    - POST /api/importaciones/ → Subir un fichero CSV
    - GET /api/importaciones/ → Listar todas las importaciones
    - POST /api/importaciones/{id}/procesar/ → Procesar/normalizar el fichero
    
    Permisos: Requiere autenticación y permisos de importación.
    """
    queryset = ImportacionHuella.objects.all()
    serializer_class = ImportacionHuellaSerializer
    pagination_class = HuellaPagination
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    # Parsers obligatorios para manejo de archivos
    parser_classes = (parsers.MultiPartParser, parsers.FormParser)

    def perform_create(self, serializer):
        """Asigna automáticamente el usuario que hace la solicitud."""
        # Si no hay usuario autenticado, usa el primer usuario (admin)
        usuario = self.request.user if self.request.user.is_authenticated else None
        if usuario is None:
            from django.contrib.auth.models import User
            usuario = User.objects.first()
        
        serializer.save(usuario=usuario)

    @action(detail=True, methods=['post'])
    def procesar(self, request, pk=None):
        """
        Procesa y normaliza el fichero CSV importado.
        
        POST /api/importaciones/{id}/procesar/
        """
        importacion = self.get_object()
        
        # Cambiar estado a procesando
        importacion.estado = 'PROCESANDO'
        importacion.save()
        
        try:
            # Ejecutar el script de normalización
            normalizar_archivo(importacion.id)
            importacion.refresh_from_db()
            return Response({
                'status': 'Procesado exitosamente',
                'estado': importacion.estado,
                'id': importacion.id
            })
        except Exception as e:
            importacion.estado = 'ERROR'
            importacion.log_proceso += f"\n[ERROR] {str(e)}"
            importacion.save()
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['post'])
    def aplicar_correcciones(self, request, pk=None):
        """
        Aplica las correcciones manuales a los registros con errores.
        
        POST /api/importaciones/{id}/aplicar_correcciones/
        Body: archivo CSV con correcciones
        """
        importacion = self.get_object()
        
        try:
            # Procesar el archivo de correcciones
            if 'correcciones' in request.FILES:
                archivo = request.FILES['correcciones']
                correcciones = {}
                
                for linea in archivo.read().decode('utf-8').split('\n'):
                    if linea.strip():
                        partes = linea.split('|')
                        if len(partes) >= 2:
                            num_linea = partes[0].strip()
                            valor = partes[1].strip()
                            correcciones[num_linea] = valor
                
                # Guardar correcciones en el log
                importacion.log_proceso += f"\n[CORRECCIONES APLICADAS] {len(correcciones)} registros"
                importacion.save()
                
                return Response({
                    'status': 'Correcciones aplicadas',
                    'cantidad': len(correcciones)
                })
            else:
                return Response(
                    {'error': 'No se envió archivo de correcciones'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# =======================================================
# VISTAS DE AUTENTICACIÓN
# =======================================================

from django.contrib.auth.models import User


class LoginView(APIView):
    """
    Endpoint para login de usuarios.
    
    POST /api/auth/login/
    {
        "username": "usuario",
        "password": "contraseña"
    }
    
    Respuesta:
    {
        "token": "abc123...",
        "user": {
            "id": 1,
            "username": "usuario",
            "email": "user@example.com",
            "grupos": ["Admin"],
            "permisos": [...]
        }
    }
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data
        })


class LogoutView(APIView):
    """
    Endpoint para logout de usuarios.
    
    POST /api/auth/logout/
    Headers: Authorization: Token abc123...
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        try:
            request.user.auth_token.delete()
        except:
            pass
        
        return Response({
            'message': 'Sesión cerrada exitosamente'
        })


class UserDetailView(APIView):
    """
    Endpoint para obtener información del usuario autenticado.
    
    GET /api/auth/me/
    Headers: Authorization: Token abc123...
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class MenuView(APIView):
    """
    Endpoint para obtener la configuración de menú según el rol del usuario.
    
    GET /api/auth/menu/
    Headers: Authorization: Token abc123...
    
    Respuesta:
    {
        "mostrar_huellas": true,
        "mostrar_importar": true,
        "mostrar_reportes": false,
        "mostrar_usuarios": false,
        "mostrar_resolucion": false
    }
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user)
        menu = serializer.data.get('menu', {})
        return Response(menu)

class IsAdminOrIngenieria(IsAuthenticated):
    """Permiso para Admin e Ingeniería - acceso total."""
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
        user_groups = request.user.groups.values_list('name', flat=True)
        return 'Admin' in user_groups or 'Ingenieria' in user_groups


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestión de usuarios.
    
    Permisos:
    - Admin/Ingeniería: CRUD completo de todos los usuarios
    - Otros roles: Solo pueden ver y editar su propio usuario
    
    Endpoints:
    - GET /api/usuarios/ - Listar usuarios (Admin/Ing: todos, otros: solo él)
    - POST /api/usuarios/ - Crear usuario (solo Admin/Ing)
    - GET /api/usuarios/{id}/ - Ver usuario
    - PUT/PATCH /api/usuarios/{id}/ - Editar usuario
    - DELETE /api/usuarios/{id}/ - Desactivar usuario (solo Admin/Ing)
    - GET /api/usuarios/roles/ - Listar roles disponibles
    - POST /api/usuarios/{id}/activar/ - Reactivar usuario
    """
    queryset = User.objects.all().select_related('profile')
    serializer_class = UserManagementSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        """
        Filtra usuarios según el rol del usuario actual.
        Admin/Ingeniería ven todos, otros solo se ven a sí mismos.
        """
        user = self.request.user
        user_groups = user.groups.values_list('name', flat=True)
        
        if 'Admin' in user_groups or 'Ingenieria' in user_groups:
            # Admin e Ingeniería ven todos los usuarios
            return User.objects.all().select_related('profile').order_by('-date_joined')
        else:
            # Otros usuarios solo se ven a sí mismos
            return User.objects.filter(id=user.id).select_related('profile')

    def create(self, request, *args, **kwargs):
        """Solo Admin/Ingeniería pueden crear usuarios."""
        user_groups = request.user.groups.values_list('name', flat=True)
        if 'Admin' not in user_groups and 'Ingenieria' not in user_groups:
            return Response(
                {'error': 'No tiene permisos para crear usuarios'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Admin/Ingeniería pueden editar cualquier usuario.
        Otros usuarios solo pueden editar su propio perfil (campos limitados).
        """
        instance = self.get_object()
        user_groups = request.user.groups.values_list('name', flat=True)
        
        is_admin = 'Admin' in user_groups or 'Ingenieria' in user_groups
        is_own_profile = instance.id == request.user.id
        
        if not is_admin and not is_own_profile:
            return Response(
                {'error': 'No tiene permisos para editar este usuario'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Si no es admin, limitar campos editables
        if not is_admin:
            allowed_fields = ['email', 'first_name', 'last_name', 'password']
            # También permitir telefono del profile
            for key in list(request.data.keys()):
                if key not in allowed_fields and key != 'telefono':
                    del request.data[key]
        
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Desactiva el usuario en lugar de eliminarlo (soft delete).
        Solo Admin/Ingeniería pueden desactivar usuarios.
        """
        user_groups = request.user.groups.values_list('name', flat=True)
        if 'Admin' not in user_groups and 'Ingenieria' not in user_groups:
            return Response(
                {'error': 'No tiene permisos para desactivar usuarios'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        instance = self.get_object()
        
        # No permitir desactivarse a sí mismo
        if instance.id == request.user.id:
            return Response(
                {'error': 'No puede desactivar su propio usuario'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Soft delete: desactivar en lugar de eliminar
        instance.is_active = False
        instance.save()
        
        if hasattr(instance, 'profile'):
            instance.profile.is_active_profile = False
            instance.profile.save()
        
        return Response(
            {'message': f'Usuario {instance.username} desactivado correctamente'},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'])
    def activar(self, request, pk=None):
        """Reactiva un usuario desactivado."""
        user_groups = request.user.groups.values_list('name', flat=True)
        if 'Admin' not in user_groups and 'Ingenieria' not in user_groups:
            return Response(
                {'error': 'No tiene permisos para activar usuarios'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        instance = self.get_object()
        instance.is_active = True
        instance.save()
        
        if hasattr(instance, 'profile'):
            instance.profile.is_active_profile = True
            instance.profile.save()
        
        return Response(
            {'message': f'Usuario {instance.username} activado correctamente'},
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['get'])
    def roles(self, request):
        """Lista todos los roles/grupos disponibles."""
        grupos = Group.objects.all()
        serializer = GroupSerializer(grupos, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def me(self, request):
        """Obtiene información del usuario actual."""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
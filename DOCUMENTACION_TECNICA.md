# HUELLA APP - Documentación Técnica Completa

## 📋 Índice
1. [Visión General](#visión-general)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Backend (Django REST)](#backend-django-rest)
4. [Frontend (React + Vite)](#frontend-react--vite)
5. [Integración (Cómo se Unen)](#integración-cómo-se-unen)
6. [Flujo de Datos](#flujo-de-datos)
7. [Deployment](#deployment)
8. [Seguridad](#seguridad)

---

## Visión General

**HUELLA APP** es una aplicación web moderna de **dos capas** (cliente-servidor) diseñada para gestionar **líneas de domicilios** (infraestructura de telecomunicaciones) con capacidad de:

- ✓ Registrar y visualizar 36 campos de información por línea
- ✓ Filtrar y buscar mediante API REST
- ✓ Importar datos desde archivos CSV
- ✓ Proporcionar una interfaz intuitiva y responsiva

**Stack Tecnológico:**
- **Backend:** Django 4.2 + Django REST Framework (Python)
- **Frontend:** React 18 + Vite (JavaScript/JSX)
- **Base de Datos:** SQLite (desarrollo), PostgreSQL (producción)
- **API:** REST con paginación, filtrado y búsqueda avanzada

---

## Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────┐
│                    USUARIO (Navegador Web)                  │
└──────────────────────────┬──────────────────────────────────┘
                           │
                    HTTP/HTTPS (puerto 5173)
                           │
        ┌──────────────────▼──────────────────┐
        │   FRONTEND (React + Vite)           │
        │   - Interfaz de usuario             │
        │   - Gestión de estado               │
        │   - Validación cliente              │
        │   http://localhost:5173             │
        └──────────────────┬──────────────────┘
                           │
            REST API (HTTP GET, POST, PUT, DELETE)
              CORS: Cross-Origin Resource Sharing
                           │
        ┌──────────────────▼──────────────────┐
        │    BACKEND (Django REST)            │
        │    - API REST (8000)                │
        │    - Lógica de negocio              │
        │    - Validación servidor            │
        │    - Autenticación/Autorización     │
        │    http://localhost:8000            │
        └──────────────────┬──────────────────┘
                           │
                 ORM (Object-Relational Mapping)
                           │
        ┌──────────────────▼──────────────────┐
        │   BASE DE DATOS                     │
        │   - SQLite (dev)                    │
        │   - PostgreSQL (prod)               │
        │   - Tabla: huella_app_huella        │
        │   - 36 campos de datos              │
        └─────────────────────────────────────┘
```

---

## Backend (Django REST)

### 📁 Estructura de Carpetas

```
huella_project/
├── huella_project/              # Configuración principal
│   ├── settings.py              # Configuración de Django
│   ├── urls.py                  # Rutas principales
│   ├── wsgi.py                  # Interfaz WSGI (producción)
│   └── asgi.py                  # Interfaz ASGI (async)
│
└── huella_app/                  # Aplicación Django
    ├── models.py                # Modelo Huella (36 campos)
    ├── serializers.py           # Conversión de datos Python ↔ JSON
    ├── views.py                 # Lógica API (ViewSets)
    ├── urls.py                  # Rutas de /api/
    ├── admin.py                 # Panel administrativo
    ├── apps.py                  # Configuración de la app
    ├── management/
    │   └── commands/
    │       └── import_huella_csv.py  # Comando para importar CSV
    └── migrations/              # Cambios de base de datos
```

### 🔑 Componentes Clave

#### 1. **Modelo (models.py)**
Define la estructura de datos de una "Huella" (línea de domicilio).

```python
class Huella(models.Model):
    # Campo único e indexado
    iddomicilioto = models.CharField(max_length=50, unique=True, db_index=True)
    
    # Obligatorios
    codigopostal = models.CharField(max_length=5, db_index=True)
    provincia = models.CharField(max_length=22, db_index=True)
    poblacion = models.CharField(max_length=255, db_index=True)
    
    # Dirección
    tipovia = models.CharField(max_length=17)
    nombrevia = models.CharField(max_length=255)
    numero = models.CharField(max_length=5, blank=True)
    
    # Infraestructura (indexada para búsquedas)
    codigoolt = models.CharField(max_length=23, db_index=True, blank=True)
    codigocto = models.CharField(max_length=15, db_index=True, blank=True)
    
    # ... 24 campos más ...
    
    # Auditoría automática
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
```

**Ventajas:**
- Validación a nivel de BD
- Índices para búsquedas rápidas
- Timestamps automáticos para auditoría

#### 2. **Serializador (serializers.py)**
Convierte modelos Python a JSON y viceversa.

```python
class HuellaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Huella
        fields = [36 campos aquí]
        read_only_fields = ['id', 'created', 'updated']
```

**Flujo:**
```
Modelo Django (Python) 
    ↓ (serializer.dump)
JSON (texto plano)
    ↓ (HTTP response)
Navegador (React)
```

#### 3. **Vista/ViewSet (views.py)**
Define los endpoints de la API REST.

```python
class HuellaViewSet(viewsets.ModelViewSet):
    queryset = Huella.objects.all()
    serializer_class = HuellaSerializer
    
    # Filtrado automático
    filterset_fields = ['codigopostal', 'provincia', 'poblacion']
    
    # Búsqueda en múltiples campos
    search_fields = ['iddomicilioto', 'nombrevia', 'provincia']
    
    # Ordenamiento
    ordering_fields = ['created', 'nombrevia']
```

**Endpoints automáticos generados:**
```
GET    /api/huellas/               → Listar (paginado)
POST   /api/huellas/               → Crear
GET    /api/huellas/{id}/          → Ver detalle
PUT    /api/huellas/{id}/          → Actualizar
DELETE /api/huellas/{id}/          → Eliminar
```

#### 4. **Rutas (urls.py)**
Mapea URLs a viewsets.

```python
router = DefaultRouter()
router.register(r'huellas', HuellaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
```

### 📊 Flujo de Datos en el Backend

**Lectura (GET):**
```
Usuario hace clic "Buscar"
         ↓
React envía: GET /api/huellas/?search=FENE
         ↓
Django recibe request
         ↓
ViewSet ejecuta .list()
         ↓
QuerySet filtra la BD
         ↓
Serializer convierte a JSON
         ↓
Django devuelve JSON response (200 OK)
         ↓
React recibe y renderiza
```

**Creación (POST):**
```
Usuario rellena formulario
         ↓
React valida datos localmente
         ↓
React envía: POST /api/huellas/ + JSON
         ↓
Django recibe request + JSON
         ↓
ViewSet ejecuta .create()
         ↓
Serializer valida datos
         ↓
Modelo guarda en BD
         ↓
Serializer convierte a JSON
         ↓
Django devuelve JSON + status 201 (Created)
         ↓
React actualiza lista
```

### 🔐 Autenticación y CORS

**settings.py:**
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  # React dev
    "http://localhost:3000",   # Otros puertos
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',  # Sin autenticación (por ahora)
    ],
}
```

---

## Frontend (React + Vite)

### 📁 Estructura de Carpetas

```
frontend/
├── src/
│   ├── main.jsx                 # Punto de entrada
│   ├── App.jsx                  # Componente raíz
│   ├── styles.css               # Estilos globales
│   └── components/
│       └── HuellaList.jsx        # Componente principal (lista + filtros)
├── index.html                   # HTML base
├── vite.config.js               # Configuración de Vite
├── package.json                 # Dependencias Node
└── package-lock.json            # Versiones exactas de dependencias
```

### 🔑 Componentes

#### 1. **main.jsx - Punto de Entrada**
```javascript
import React from 'react'
import { createRoot } from 'react-dom/client'
import App from './App'
import './styles.css'

createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
)
```

Monta la aplicación React en el `<div id="root">` del HTML.

#### 2. **App.jsx - Componente Raíz**
```javascript
export default function App(){
  return (
    <div className="app">
      <header><h1>Huella App</h1></header>
      <main>
        <HuellaList />
      </main>
    </div>
  )
}
```

Estructura básica de la aplicación.

#### 3. **HuellaList.jsx - Componente Principal**
El corazón de la interfaz. Incluye:

**Estado (Hooks):**
```javascript
const [huellas, setHuellas] = useState([])          // Datos de la BD
const [loading, setLoading] = useState(false)       // Indicador de carga
const [error, setError] = useState(null)            // Mensajes de error
const [search, setSearch] = useState('')            // Campo de búsqueda
const [codigopostal, setCodigopostal] = useState('') // Filtro CP
const [provincia, setProvincia] = useState('')      // Filtro provincia
const [poblacion, setPoblacion] = useState('')      // Filtro población
const [page, setPage] = useState(1)                 // Página actual
const [pageSize, setPageSize] = useState(50)        // Resultados/página
```

**Funciones principales:**
```javascript
fetchHuellas()          // Consulta API y actualiza estado
handleSearchSubmit()    // Ejecuta búsqueda al hacer clic
clearFilters()          // Limpia todos los filtros
renderTable()           # Dibuja la tabla HTML con datos
```

**Interfaz:**
- Campos de entrada para filtros (search, CP, provincia, población)
- Botones: Buscar, Limpiar
- Selector de resultados por página
- Tabla con columnas (ID, CP, Provincia, Población, Vía, Número, OLT, CTO)
- Paginación (Anterior/Siguiente)

### 📊 Flujo de Datos en el Frontend

**Cargar datos al iniciar:**
```
useEffect() se ejecuta
         ↓
fetchHuellas() es llamado
         ↓
axios.get('/api/huellas/?page=1&page_size=50')
         ↓
Backend responde con JSON
         ↓
setHuellas(data.results)  ← Actualiza estado
         ↓
Componente re-renderiza
         ↓
renderTable() dibuja <table> con datos
         ↓
Usuario ve tabla en pantalla
```

**Buscar:**
```
Usuario escribe en campo de búsqueda
         ↓
setSearch(value)  ← Actualiza estado local
         ↓
Usuario hace clic "Buscar"
         ↓
handleSearchSubmit() → setPage(1) + fetchHuellas()
         ↓
fetchHuellas() construye params: {search, codigopostal, provincia, ...}
         ↓
axios.get('/api/huellas/', { params })  ← URL con query string
         ↓
Backend filtra en BD
         ↓
Respuesta con resultados filtrados
         ↓
setHuellas() actualiza estado
         ↓
Tabla re-renderiza con nuevos datos
```

### 🎨 Tecnologías Frontend

| Librería | Versión | Propósito |
|----------|---------|-----------|
| React | 18.2.0 | Interfaz de usuario (componentes) |
| Vite | 5.0.0 | Bundler y servidor de desarrollo |
| Axios | 1.4.0 | Cliente HTTP para llamadas a la API |
| CSS | Vanilla | Estilos (sin frameworks adicionales) |

---

## Integración: Cómo se Unen

### 1. **El Flujo Completo (Búsqueda de Huellas)**

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Usuario abre http://localhost:5173 en el navegador       │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. React carga (App.jsx → HuellaList.jsx)                  │
│    useEffect() ejecuta fetchHuellas()                       │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. axios.get('http://localhost:8000/api/huellas/?page=1')  │
│    Petición HTTP GET con query parameters                  │
└──────────────────────┬──────────────────────────────────────┘
                       │
            ┌──────────┴──────────┐
            │                     │ (pasa por CORS)
            ▼                     ▼
┌──────────────────────────────────────────────────────────────┐
│ 4. Django recibe request en urls.py → encamina a ViewSet    │
│    HuellaViewSet.list() filtra con parámetros               │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────────┐
│ 5. BD ejecuta query: SELECT * FROM huella_app_huella        │
│    Filtra por search, codigopostal, etc.                    │
│    Limita a 50 resultados (page_size)                       │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────────┐
│ 6. Django serializa resultados a JSON                        │
│    Response: {count: 100, results: [{id: 1, ...}, ...]}     │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────────┐
│ 7. Viaja a través de HTTP/REST (pasa por CORS)              │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────────┐
│ 8. React recibe JSON en HuellaList.jsx                      │
│    setHuellas(data.results)  ← actualiza estado             │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────────┐
│ 9. Componente re-renderiza con nuevos datos                 │
│    renderTable() dibuja <table> HTML                        │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────────┐
│ 10. Usuario ve tabla en pantalla con 50 filas               │
│     Puede cambiar página, filtrar, buscar...                │
└──────────────────────────────────────────────────────────────┘
```

### 2. **Protocolo de Comunicación**

**HTTP REST (Stateless):**
- Cada request es **independiente**
- No hay sesión (por ahora)
- Basado en métodos HTTP estándar

**Ejemplo de petición (cURL):**
```bash
curl -X GET "http://localhost:8000/api/huellas/?search=FENE&codigopostal=15035&page=1&page_size=50"
```

**Ejemplo de respuesta (JSON):**
```json
{
  "count": 6,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "iddomicilioto": "RA150541100000000000000000000000238832",
      "codigopostal": "15035",
      "provincia": "A CORUÑA",
      "poblacion": "FENE",
      "nombrevia": "LUBIAN",
      "numero": "00005",
      "codigoolt": "RA-15-NARON-02-OLT",
      "codigocto": "1505432CT0419",
      "created": "2025-11-26T12:00:00Z"
    },
    ...
  ]
}
```

### 3. **CORS (Cross-Origin Resource Sharing)**

**¿Por qué es necesario?**
- Frontend corre en `http://localhost:5173`
- Backend corre en `http://localhost:8000`
- **Diferentes orígenes** → navegador bloquea por defecto

**Solución:**
Backend incluye headers CORS:
```
Access-Control-Allow-Origin: http://localhost:5173
Access-Control-Allow-Methods: GET, POST, PUT, DELETE
Access-Control-Allow-Headers: Content-Type
```

Django lo maneja automáticamente con `django-cors-headers`.

### 4. **Flujo de Filtrado**

**En el Frontend (HuellaList.jsx):**
```javascript
const params = {
  page: 1,
  page_size: 50,
  search: 'FENE',
  codigopostal: '15035',
  provincia: 'A CORUÑA',
  poblacion: ''  // ignorado si está vacío
}
axios.get(API_URL, { params })  // axios serializa a query string
```

**URL generada:**
```
/api/huellas/?page=1&page_size=50&search=FENE&codigopostal=15035&provincia=A%20CORUÑA
```

**En el Backend (views.py):**
```python
class HuellaViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['codigopostal', 'provincia']  # filtrado exacto
    search_fields = ['nombrevia', 'provincia']        # búsqueda parcial
    
    # DRF parsea automáticamente:
    # - ?search=FENE → filtra por search_fields
    # - ?codigopostal=15035 → filtra por filterset_fields
    # - ?page=1&page_size=50 → pagina resultados
```

**Resultado en BD:**
```sql
SELECT * FROM huella_app_huella
WHERE (nombrevia ILIKE '%FENE%' OR provincia ILIKE '%FENE%')
  AND codigopostal = '15035'
  AND provincia = 'A CORUÑA'
LIMIT 50 OFFSET 0
```

---

## Flujo de Datos Detallado

### Importación de CSV

```
Usuario ejecuta:
python manage.py import_huella_csv archivo.csv

         ↓

Comando lee CSV línea a línea

         ↓

Para cada fila:
- Valida 36 columnas
- Valida campos obligatorios
- Convierte tipos de datos (lat/lng a decimal)

         ↓

Llama a Huella.objects.get_or_create()

         ↓

Django guarda en BD (o actualiza si existe)

         ↓

Muestra resumen: ✓ Creadas: 100, ⊗ Actualizadas: 5
```

### Panel Admin (http://localhost:8000/admin/)

Django proporciona automáticamente un panel CRUD:
- Listar todas las huellas
- Crear nueva huella manualmente
- Editar existente
- Eliminar
- Búsqueda y filtros

---

## Deployment (Producción)

### Backend

**1. Reemplazar BD SQLite con PostgreSQL:**
```bash
pip install psycopg2-binary
```

**settings.py:**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASSWORD'],
        'HOST': os.environ['DB_HOST'],
        'PORT': '5432',
    }
}
```

**2. Usar servidor WSGI (Gunicorn):**
```bash
pip install gunicorn
gunicorn huella_project.wsgi:application --bind 0.0.0.0:8000
```

**3. Configurar Nginx como proxy inverso:**
```nginx
server {
    listen 80;
    server_name api.ejemplo.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Frontend

**1. Construir para producción:**
```bash
npm run build  # Genera carpeta dist/ con archivos minificados
```

**2. Servir desde Nginx:**
```nginx
server {
    listen 80;
    server_name ejemplo.com;

    location / {
        root /var/www/huella-app/dist;
        try_files $uri $uri/ /index.html;  # SPA routing
    }

    location /api/ {
        proxy_pass http://api.ejemplo.com;
    }
}
```

---

## Seguridad

### Medidas Implementadas

1. **CORS configurado:** Solo orígenes permitidos
2. **HTTPS recomendado:** En producción, usar SSL/TLS
3. **Validación servidor:** Django valida TODOS los datos
4. **Índices de BD:** Para evitar escaneos de tabla completa
5. **Timestamps de auditoría:** created/updated para tracking

### Mejoras Futuras

1. **Autenticación:** OAuth2, JWT tokens
2. **Autorización:** Roles y permisos (admin, editor, viewer)
3. **Rate limiting:** Limitar peticiones por IP
4. **Logging:** Auditoría de cambios
5. **Encriptación:** Datos sensibles encriptados

---

## Resumen

| Aspecto | Backend | Frontend |
|--------|---------|----------|
| **Lenguaje** | Python | JavaScript/JSX |
| **Framework** | Django 4.2 | React 18 |
| **Puerto** | 8000 | 5173 |
| **Funciones** | Lógica, BD, validación | UI, UX, validación local |
| **Almacena** | Datos en BD | Estado en memoria |
| **Comunicación** | HTTP REST API | axios (HTTP client) |
| **Escalabilidad** | Horizontal (múltiples servidores) | CDN para assets estáticos |

**Flujo de datos resumido:**
```
Usuario (Navegador)
    ↓
React (Interfaz)
    ↓ (Petición HTTP)
Django REST (API)
    ↓ (Query)
PostgreSQL (Base de Datos)
```

Todo está diseñado para ser **modular**, **escalable** y **fácil de mantener**.

---

## Notas para Presentación Empresarial

✓ **Arquitectura moderna:** Separación clara cliente-servidor
✓ **Stack probado:** Django y React son tecnologías empresariales de confianza
✓ **Escalable:** Fácil agregar más features, usuarios, datos
✓ **Mantenible:** Código estructurado y documentado
✓ **Seguro:** Validación en cliente y servidor
✓ **Performante:** Índices de BD, paginación, caching posible
✓ **Responsive:** Interfaz se adapta a cualquier dispositivo


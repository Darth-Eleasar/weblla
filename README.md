# Huella App - Gestión de Líneas de Domicilios

Aplicación Django REST Framework para gestionar líneas de huella (domicilios) basada en el formato estándar CH.

## Características

- ✅ Modelo completo con 36 campos según estándar CH
- ✅ API REST completa con CRUD
- ✅ Filtrado avanzado por múltiples criterios
- ✅ Búsqueda en tiempo real
- ✅ Endpoints especializados para consultas comunes
- ✅ Importación desde CSV con validación
- ✅ Admin Django personalizado
- ✅ Paginación configurable
- ✅ CORS habilitado

## Requisitos

- Python 3.8+
- Django 4.2+
- Django REST Framework 3.14+
- psycopg 3.1+
- dj-database-url 2.1+
- gunicorn 21.2+
- whitenoise 6.4+

## Instalación

1. **Clonar o descargar el proyecto:**

```bash
Colocarnos en el directorio donde queramos clonar la app
git clone url_repositorio
cd cd weblla
```

2. **Herramientas necesarias:**

- ✅ Git
- ✅ Docker Desktop (para Windows/Mac) o Docker Engine (Linux)
- ✅ Python 3.12 o superior
- ✅ Node.js 18 o superior
- ✅ Visual Studio Code

3. **Crear entorno virtual (sólo en desarrollo local):**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

3.1 **Comandos iniciales:**

| Entorno | Comando | Función |
|---------|----------------------------------------------|---------------------------------------|
| Local | pip install -r requirements.txt | 4. Instalar dependencias |
| Servidor | docker compose exec backend pip install -r requirements.txt | 4. Instalar dependencias |
| Local | python manage.py migrate | 5. Aplicar Migraciones |
| Servidor | docker compose exec backend python manage.py migrate | 5. Aplicar Migraciones |
| Local | python manage.py createsuperuser | 6. Crear Superusuario (opcional) |
| Servidor | docker compose exec backend python manage.py createsuperuser | 6. Crear Superusuario (opcional) |
| Local | docker compose -f docker-compose.dev.yml up -d | 7. Iniciar servidor Docker |
| Servidor | docker compose -f docker-compose.yml up -d -build | 7. Iniciar servidor Docker |
| Local | python manage.py crear_roles | 8. Crea Grupos, roles y permisos |
| Servidor | docker compose exec backend python manage.py crear_roles | 8. Crea Grupos, roles y permisos |
| Local | python manage.py assign_admin_role | 9. Asigna grupo y permisos completos al usuario admin |
| Servidor | docker compose exec backend python manage.py assign_admin_role | 9. Asigna grupo y permisos completos al usuario admin |

Se puede usar python manage.py assign_admin_role --username nombre_usuario, si queremos asignar los permisos de administrador global a otro usuario que no se el admin.

El servidor estará disponible en: `http://localhost:8000`

## API Endpoints

### Documentación

- **Browsable API**: `http://localhost:8000/api/`
- **Admin Panel**: `http://localhost:8000/admin/`

### Huellas - CRUD Básico

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/huellas/` | Listar todas las huellas (paginado) |
| POST | `/api/huellas/` | Crear nueva huella |
| GET | `/api/huellas/{id}/` | Obtener detalle de huella |
| PUT | `/api/huellas/{id}/` | Actualizar huella |
| DELETE | `/api/huellas/{id}/` | Eliminar huella |

### Filtrado y Búsqueda

```bash
# Búsqueda general
GET /api/huellas/?search=FENE

# Filtrar por código postal
GET /api/huellas/?codigopostal=15035

# Filtrar por provincia
GET /api/huellas/?provincia=A%20CORUÑA

# Filtrar por población
GET /api/huellas/?poblacion=FENE

# Filtrar por CTO
GET /api/huellas/?codigocto=1505432CT0419

# Múltiples criterios
GET /api/huellas/?codigopostal=15035&provincia=A%20CORUÑA&search=LUBIAN
```

### Endpoints Especializados

```bash
# Huellas por código postal
GET /api/huellas/por_codigo_postal/?codigo=15035

# Huellas por provincia
GET /api/huellas/por_provincia/?provincia=A%20CORUÑA

# Huellas por población
GET /api/huellas/por_poblacion/?poblacion=FENE

# Huellas por CTO
GET /api/huellas/por_cto/?codigo=1505432CT0419

# Huellas por OLT
GET /api/huellas/por_olt/?codigo=RA-15-NARON-02-OLT

# Estadísticas globales
GET /api/huellas/estadisticas/

# Huellas vecinas (cercanas en dirección)
GET /api/huellas/{id}/vecinos/
```

### Ordenamiento

```bash
# Ordenar por fecha (descendente)
GET /api/huellas/?ordering=-created

# Ordenar por fecha (ascendente)
GET /api/huellas/?ordering=created

# Ordenar por provincia
GET /api/huellas/?ordering=provincia

# Ordenar por nombre de vía
GET /api/huellas/?ordering=nombrevia
```

### Paginación

```bash
# Página por defecto (50 resultados)
GET /api/huellas/

# Página 2
GET /api/huellas/?page=2

# 100 resultados por página
GET /api/huellas/?page_size=100
```

## Importación desde CSV

### Formato esperado

- Delimitador: `;` (punto y coma)
- 36 columnas en orden estándar CH
- Campos obligatorios: `iddomicilioto`, `codigopostal`, `provincia`, `poblacion`

### Comando de importación

```powershell
# Importación básica
python manage.py import_huella_csv ruta\archivo.csv

# Importación omitiendo errores
python manage.py import_huella_csv ruta\archivo.csv --skip-errors

# Importación con información detallada
python manage.py import_huella_csv ruta\archivo.csv --verbose

# Importación con skip-errors y verbose
python manage.py import_huella_csv ruta\archivo.csv --skip-errors --verbose

# Usar delimitador diferente
python manage.py import_huella_csv ruta\archivo.csv --delimiter=,
```

## Ejemplos de Uso

### Con cURL

```bash
# Obtener lista de huellas
curl http://localhost:8000/api/huellas/

# Búsqueda por población
curl "http://localhost:8000/api/huellas/?search=FENE"

# Obtener estadísticas
curl http://localhost:8000/api/huellas/estadisticas/

# Crear nueva huella
curl -X POST http://localhost:8000/api/huellas/ \
  -H "Content-Type: application/json" \
  -d '{
    "iddomicilioto": "RA150541100000000000000000000000238840",
    "codigopostal": "15035",
    "provincia": "A CORUÑA",
    "poblacion": "FENE",
    "tipovia": "CALLE",
    "nombrevia": "LUBIAN",
    "numero": "12"
  }'
```

### Con Python/Requests

```python
import requests

# Obtener todas las huellas
response = requests.get('http://localhost:8000/api/huellas/')
huellas = response.json()

# Filtrar por provincia
response = requests.get('http://localhost:8000/api/huellas/', params={
    'provincia': 'A CORUÑA'
})
huellas_provincia = response.json()

# Obtener estadísticas
response = requests.get('http://localhost:8000/api/huellas/estadisticas/')
stats = response.json()

# Crear nueva huella
nueva_huella = {
    'iddomicilioto': 'RA150541100000000000000000000000238840',
    'codigopostal': '15035',
    'provincia': 'A CORUÑA',
    'poblacion': 'FENE',
    'tipovia': 'CALLE',
    'nombrevia': 'LUBIAN',
    'numero': '12'
}
response = requests.post('http://localhost:8000/api/huellas/', json=nueva_huella)
print(response.json())
```

## Estructura de Campos

### Identidad (Campos 1-4)

- `iddomicilioto`: Identificador único (50 chars)
- `codigopostal`: Código postal 5 dígitos
- `provincia`: Nombre de provincia (22 chars)
- `poblacion`: Población/municipio (255 chars)

### Ubicación (Campos 5-8)

- `tipovia`: Tipo de vía (CALLE, AVENIDA, etc.)
- `nombrevia`: Nombre de la vía
- `idtecnicovia`: ID técnico de vía
- `numero`: Número de portal

### Finca (Campos 9-12)

- `bisduplicado`: Bis o duplicado
- `bloquedelafinca`: Bloque
- `identificadorfincaportal`: ID finca/portal
- `letrafinca`: Letra de finca

### Edificio (Campos 13-16)

- `escalera`: Escalera
- `planta`: Piso/planta
- `mano1`: Primera mano/puerta
- `mano2`: Segunda mano/puerta

### Infraestructura (Campos 22-25)

- `codigoolt`: OLT (Optical Line Terminal)
- `codigocto`: CTO (Central Terminal Office)
- `tipocto`: Tipo de CTO
- `direccioncto`: Dirección de CTO

### Localización (Campos 35-36)

- `lat`: Latitud (decimal)
- `lng`: Longitud (decimal)

## Campos Completos (36 campos)

1. iddomicilioto
2. codigopostal
3. provincia
4. poblacion
5. tipovia
6. nombrevia
7. idtecnicovia
8. numero
9. bisduplicado
10. bloquedelafinca
11. identificadorfincaportal
12. letrafinca
13. escalera
14. planta
15. mano1
16. mano2
17. observaciones
18. flagdummy
19. codigoinevia
20. codigocensal
21. codigopai
22. codigoolt
23. codigocto
24. tipocto
25. direccioncto
26. tipopermiso
27. tipocajaderivacion
28. numunidadesinmobiliarias
29. numviviendas
30. fechaalta
31. codigocajaderivacion
32. ubicacioncajaderivacion
33. coinv
34. area_comercial
35. lat
36. lng

## Respuesta de API

### Ejemplo de Huella Completa

```json
{
  "id": 1,
  "iddomicilioto": "RA150541100000000000000000000000238832",
  "codigopostal": "15035",
  "provincia": "A CORUÑA",
  "poblacion": "FENE",
  "tipovia": "CALLE",
  "nombrevia": "LUBIAN",
  "idtecnicovia": "150074013390",
  "numero": "00005",
  "bisduplicado": "",
  "bloquedelafinca": "",
  "identificadorfincaportal": "",
  "letrafinca": "",
  "escalera": "",
  "planta": "",
  "mano1": "BA",
  "mano2": "",
  "observaciones": "",
  "flagdummy": "",
  "codigoinevia": "",
  "codigocensal": "",
  "codigopai": "",
  "codigoolt": "RA-15-NARON-02-OLT",
  "codigocto": "1505432CT0419",
  "tipocto": "CT8",
  "direccioncto": "LUBIAN 10",
  "tipopermiso": "POSTE",
  "tipocajaderivacion": "",
  "numunidadesinmobiliarias": "1",
  "numviviendas": "1",
  "fechaalta": "20251031",
  "codigocajaderivacion": "",
  "ubicacioncajaderivacion": "",
  "coinv": "",
  "area_comercial": "",
  "lat": null,
  "lng": null,
  "created": "2025-11-26T12:00:00Z",
  "updated": "2025-11-26T12:00:00Z"
}
```

## Configuración en Producción

### Variables de Entorno

```bash
DJANGO_SECRET_KEY=tu-clave-secreta
DEBUG=False
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com
DATABASE_URL=postgresql://user:password@localhost/huella_db
CORS_ALLOWED_ORIGINS=https://tu-dominio.com,https://www.tu-dominio.com
```

### Base de datos PostgreSQL

```python
# En settings.py para producción
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'huella_db'),
        'USER': os.environ.get('DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}
```

## Troubleshooting

### Problema: "ImportError: No module named 'rest_framework'"

**Solución:**
```powershell
pip install -r requirements.txt
```

### Problema: "django.core.exceptions.ImproperlyConfigured"

**Solución:** Asegúrate de que `huella_app` está en `INSTALLED_APPS` en `settings.py`

### Problema: Migraciones no aplicadas

**Solución:**
```powershell
python manage.py makemigrations
python manage.py migrate
```

## Licencia

Este proyecto está disponible bajo licencia MIT.

## Soporte

Para reportar problemas o sugerencias, contacta al equipo de desarrollo.

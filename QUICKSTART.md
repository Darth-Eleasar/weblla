# Quick Start - Inicio Rápido

## 1. Configuración Inicial (Windows PowerShell)

```powershell
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
.\venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt
```

## 2. Preparar Base de Datos

```powershell
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate
```

## 3. Crear Superusuario (Opcional - para acceder al admin)

```powershell
python manage.py createsuperuser
```

## 4. Iniciar Servidor

```powershell
python manage.py runserver
```

Accede a:
- **API**: http://localhost:8000/api/
- **Admin**: http://localhost:8000/admin/
- **Browsable API**: http://localhost:8000/api/huellas/

## 5. Importar Datos de Prueba

```powershell
# Importar CSV de ejemplo
python manage.py import_huella_csv ejemplo_datos.csv

# Con información detallada
python manage.py import_huella_csv ejemplo_datos.csv --verbose
```

## 6. Prueba la API

### Listar todas las huellas
```powershell
curl http://localhost:8000/api/huellas/
```

### Buscar por población
```powershell
curl "http://localhost:8000/api/huellas/?search=FENE"
```

### Obtener estadísticas
```powershell
curl http://localhost:8000/api/huellas/estadisticas/
```

### Filtrar por código postal
```powershell
curl "http://localhost:8000/api/huellas/?codigopostal=15035"
```

### Filtrar por provincia
```powershell
curl "http://localhost:8000/api/huellas/?provincia=A%20CORUÑA"
```

## Endpoints Principales

| Endpoint | Descripción |
|----------|-------------|
| `GET /api/huellas/` | Listar huellas (con paginación) |
| `POST /api/huellas/` | Crear nueva huella |
| `GET /api/huellas/{id}/` | Obtener detalle |
| `PUT /api/huellas/{id}/` | Actualizar huella |
| `DELETE /api/huellas/{id}/` | Eliminar huella |
| `GET /api/huellas/por_codigo_postal/?codigo=15035` | Por código postal |
| `GET /api/huellas/por_provincia/?provincia=A%20CORUÑA` | Por provincia |
| `GET /api/huellas/por_poblacion/?poblacion=FENE` | Por población |
| `GET /api/huellas/por_cto/?codigo=1505432CT0419` | Por CTO |
| `GET /api/huellas/estadisticas/` | Estadísticas globales |

## Campos del Modelo (36 campos)

### Obligatorios
- iddomicilioto
- codigopostal
- provincia
- poblacion

### Ubicación
- tipovia, nombrevia, numero, idtecnicovia

### Finca
- bisduplicado, bloquedelafinca, identificadorfincaportal, letrafinca

### Edificio
- escalera, planta, mano1, mano2

### Técnicos
- codigoinevia, codigocensal, codigopai, codigoolt, codigocto, tipocto, direccioncto

### Infraestructura
- tipopermiso, tipocajaderivacion, codigocajaderivacion, ubicacioncajaderivacion

### Inmobiliario
- numunidadesinmobiliarias, numviviendas

### Ubicación Geográfica
- lat, lng

### Metadatos
- fechaalta, flagdummy, coinv, area_comercial, observaciones

## Ejemplo de Creación desde API

```bash
curl -X POST http://localhost:8000/api/huellas/ \
  -H "Content-Type: application/json" \
  -d '{
    "iddomicilioto": "RA150541100000000000000000000000999999",
    "codigopostal": "15035",
    "provincia": "A CORUÑA",
    "poblacion": "FENE",
    "tipovia": "CALLE",
    "nombrevia": "MAYOR",
    "numero": "25",
    "codigoolt": "RA-15-TEST",
    "codigocto": "150TEST"
  }'
```

## Parametros de Filtrado

### Búsqueda general
```
?search=FENE
```

### Filtro por campo
```
?codigopostal=15035
?provincia=A%20CORUÑA
?poblacion=FENE
?codigoolt=RA-15-NARON-02-OLT
```

### Ordenamiento
```
?ordering=-created    # Más recientes primero
?ordering=nombrevia   # Alfabético por vía
```

### Paginación
```
?page=1               # Primera página
?page_size=100        # 100 resultados por página
```

## Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'django'"
```powershell
pip install -r requirements.txt
```

### Erro: "No such table: huella_app_huella"
```powershell
python manage.py migrate
```

### Erro: CORS (desde cliente web)
Verifica `CORS_ALLOWED_ORIGINS` en `settings.py`

## Detener Servidor
```powershell
Ctrl+C
```

## Desactivar Entorno Virtual
```powershell
deactivate
```

¡Listo! La API está lista para usar.

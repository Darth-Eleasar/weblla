# REFERENCIA RÁPIDA - Comandos y Endpoints

## INSTALACIÓN Y SETUP (5 minutos)

```powershell
# 1. Activar entorno virtual
.\venv\Scripts\Activate.ps1

# 2. Instalar paquetes
pip install -r requirements.txt

# 3. Migraciones
python manage.py migrate

# 4. Iniciar servidor
python manage.py runserver
```

## URLs PRINCIPALES

| URL | Propósito |
|-----|-----------|
| http://localhost:8000/api/ | API Browsable (explorador) |
| http://localhost:8000/admin/ | Panel Admin Django |
| http://localhost:8000/api/huellas/ | Listar huellas |

## ENDPOINTS MÁS USADOS

### Listar y Buscar
```
GET /api/huellas/                              # Lista completa
GET /api/huellas/?page=2&page_size=100         # Paginado
GET /api/huellas/?search=FENE                  # Buscar
GET /api/huellas/?codigopostal=15035           # Filtro código postal
GET /api/huellas/?provincia=A%20CORUÑA         # Filtro provincia
GET /api/huellas/?poblacion=FENE               # Filtro población
GET /api/huellas/?ordering=-created            # Ordenar descendente
```

### Crear, Actualizar, Eliminar
```
POST /api/huellas/                             # Crear
GET /api/huellas/{id}/                         # Ver detalles
PUT /api/huellas/{id}/                         # Actualizar
DELETE /api/huellas/{id}/                      # Eliminar
```

### Endpoints Especiales
```
GET /api/huellas/estadisticas/                 # Stats globales
GET /api/huellas/{id}/vecinos/                 # Huellas cercanas
GET /api/huellas/por_codigo_postal/?codigo=X   # Por código postal
GET /api/huellas/por_provincia/?provincia=X    # Por provincia
GET /api/huellas/por_poblacion/?poblacion=X    # Por población
GET /api/huellas/por_cto/?codigo=X             # Por CTO
GET /api/huellas/por_olt/?codigo=X             # Por OLT
```

## COMANDOS DJANGO ÚTILES

```powershell
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Shell interactivo
python manage.py shell

# Estadísticas de la BD
python manage.py dbshell

# Ver URLs disponibles
python manage.py show_urls

# Recolectar archivos estáticos
python manage.py collectstatic
```

## IMPORTAR DATOS CSV

```powershell
# Básico
python manage.py import_huella_csv archivo.csv

# Saltando errores
python manage.py import_huella_csv archivo.csv --skip-errors

# Con información detallada
python manage.py import_huella_csv archivo.csv --verbose

# Con skip + verbose
python manage.py import_huella_csv archivo.csv --skip-errors --verbose

# Delimitador diferente
python manage.py import_huella_csv archivo.csv --delimiter=,
```

## FORMATO CSV ESPERADO

```
COLUMNAS (36): separadas por ";"
iddomicilioto;codigopostal;provincia;poblacion;tipovia;nombrevia;...

OBLIGATORIOS:
- iddomicilioto (único)
- codigopostal
- provincia
- poblacion

EJEMPLO:
RA150541100000000000000000000000238832;15035;A CORUÑA;FENE;CALLE;LUBIAN;...
```

## EJEMPLOS CON cURL

```bash
# Listar
curl http://localhost:8000/api/huellas/

# Búsqueda
curl "http://localhost:8000/api/huellas/?search=FENE"

# Crear
curl -X POST http://localhost:8000/api/huellas/ \
  -H "Content-Type: application/json" \
  -d '{
    "iddomicilioto": "RA...",
    "codigopostal": "15035",
    "provincia": "A CORUÑA",
    "poblacion": "FENE",
    "tipovia": "CALLE",
    "nombrevia": "LUBIAN",
    "numero": "10"
  }'

# Actualizar
curl -X PUT http://localhost:8000/api/huellas/1/ \
  -H "Content-Type: application/json" \
  -d '{"observaciones": "Actualizado"}'

# Eliminar
curl -X DELETE http://localhost:8000/api/huellas/1/

# Estadísticas
curl http://localhost:8000/api/huellas/estadisticas/
```

## EJEMPLOS CON Python/Requests

```python
import requests

# Listar
r = requests.get('http://localhost:8000/api/huellas/')
huellas = r.json()

# Búsqueda
r = requests.get('http://localhost:8000/api/huellas/', params={'search': 'FENE'})

# Crear
data = {
    'iddomicilioto': 'RA...',
    'codigopostal': '15035',
    'provincia': 'A CORUÑA',
    'poblacion': 'FENE',
    'tipovia': 'CALLE',
    'nombrevia': 'LUBIAN'
}
r = requests.post('http://localhost:8000/api/huellas/', json=data)

# Detalle
r = requests.get('http://localhost:8000/api/huellas/1/')

# Actualizar
r = requests.put('http://localhost:8000/api/huellas/1/', 
                 json={'observaciones': 'Nuevo texto'})

# Eliminar
r = requests.delete('http://localhost:8000/api/huellas/1/')
```

## CAMPOS DEL MODELO (REFERENCIA)

| Num | Campo | Tipo | Longitud | Notas |
|-----|-------|------|----------|-------|
| 1 | iddomicilioto | Char | 50 | ÚNICO, Obligatorio |
| 2 | codigopostal | Char | 5 | Obligatorio |
| 3 | provincia | Char | 22 | Obligatorio |
| 4 | poblacion | Char | 255 | Obligatorio |
| 5 | tipovia | Char | 17 | - |
| 6 | nombrevia | Char | 255 | - |
| 7 | idtecnicovia | Char | 12 | - |
| 8 | numero | Char | 5 | - |
| 9 | bisduplicado | Char | 1 | - |
| 10 | bloquedelafinca | Char | 8 | - |
| 11 | identificadorfincaportal | Char | 3 | - |
| 12 | letrafinca | Char | 1 | - |
| 13 | escalera | Char | 2 | - |
| 14 | planta | Char | 3 | - |
| 15 | mano1 | Char | 4 | - |
| 16 | mano2 | Char | 4 | - |
| 17 | observaciones | Text | - | - |
| 18 | flagdummy | Char | 1 | - |
| 19 | codigoinevia | Char | 5 | - |
| 20 | codigocensal | Char | 10 | - |
| 21 | codigopai | Char | 18 | - |
| 22 | codigoolt | Char | 23 | Indexado |
| 23 | codigocto | Char | 15 | Indexado |
| 24 | tipocto | Char | 55 | - |
| 25 | direccioncto | Char | 255 | - |
| 26 | tipopermiso | Char | 50 | - |
| 27 | tipocajaderivacion | Char | 16 | - |
| 28 | numunidadesinmobiliarias | Char | 3 | - |
| 29 | numviviendas | Char | 3 | - |
| 30 | fechaalta | Char | 10 | Formato AAAAMMDD |
| 31 | codigocajaderivacion | Char | 50 | - |
| 32 | ubicacioncajaderivacion | Char | 255 | - |
| 33 | coinv | Char | 10 | - |
| 34 | area_comercial | Char | 255 | - |
| 35 | lat | Decimal | 10,8 | - |
| 36 | lng | Decimal | 10,8 | - |

## PARÁMETROS DE FILTRADO

| Parámetro | Ejemplo | Efecto |
|-----------|---------|--------|
| search | ?search=FENE | Busca en múltiples campos |
| codigopostal | ?codigopostal=15035 | Filtra código postal |
| provincia | ?provincia=A%20CORUÑA | Filtra provincia |
| poblacion | ?poblacion=FENE | Filtra población |
| codigoolt | ?codigoolt=RA-15-NARON | Filtra OLT |
| codigocto | ?codigocto=1505432 | Filtra CTO |
| ordering | ?ordering=-created | Ordena por campo |
| page | ?page=2 | Número de página |
| page_size | ?page_size=100 | Resultados por página |

## RESPUESTA TÍPICA

```json
{
  "count": 100,
  "next": "http://localhost:8000/api/huellas/?page=2",
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
    }
  ]
}
```

## ERRORES COMUNES

| Error | Causa | Solución |
|-------|-------|----------|
| "Port already in use" | Puerto 8000 ocupado | `python manage.py runserver 8001` |
| "ModuleNotFoundError" | Dependencias no instaladas | `pip install -r requirements.txt` |
| "No such table" | BD no migrada | `python manage.py migrate` |
| "CORS error" | Origen no permitido | Editar `CORS_ALLOWED_ORIGINS` en settings.py |
| "Permission denied" | Usuario sin permisos | Crear superusuario: `python manage.py createsuperuser` |

## DEBUGGING

```powershell
# Ver logs detallados
python manage.py runserver --verbosity=2

# Entrar a shell Django
python manage.py shell

# Ver todas las rutas
python manage.py show_urls
```

## ARCHIVOS IMPORTANTES

- `models.py` → Definición del modelo Huella
- `views.py` → Endpoints de la API
- `serializers.py` → Transformación de datos
- `urls.py` → Rutas de la app
- `admin.py` → Panel administrativo
- `settings.py` → Configuración del proyecto
- `manage.py` → Utilidad de gestión

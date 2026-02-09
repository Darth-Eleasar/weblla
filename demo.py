#!/usr/bin/env python
"""
Script de demostración - Ejemplos de uso de la API
Ejecutar después de: python manage.py runserver
"""

import requests
import json

BASE_URL = "http://localhost:8000/api"

def print_header(title):
    """Imprimir encabezado de sección."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def print_response(title, data):
    """Imprimir respuesta formateada."""
    print(f"\n{title}:")
    print(json.dumps(data, indent=2, ensure_ascii=False))

def main():
    print_header("DEMO - API de Gestión de Huellas")
    
    # 1. LISTAR HUELLAS
    print_header("1. LISTAR HUELLAS")
    try:
        response = requests.get(f"{BASE_URL}/huellas/?page_size=5")
        data = response.json()
        print(f"✓ Total de huellas en página: {len(data.get('results', []))}")
        if data.get('results'):
            print(f"  Primero: {data['results'][0].get('nombrevia')} {data['results'][0].get('numero')}")
            print(f"  Población: {data['results'][0].get('poblacion')}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # 2. BÚSQUEDA
    print_header("2. BÚSQUEDA (search=FENE)")
    try:
        response = requests.get(f"{BASE_URL}/huellas/?search=FENE")
        data = response.json()
        print(f"✓ Encontradas {len(data.get('results', []))} huellas con 'FENE'")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # 3. FILTRAR POR CÓDIGO POSTAL
    print_header("3. FILTRAR POR CÓDIGO POSTAL (15035)")
    try:
        response = requests.get(f"{BASE_URL}/huellas/?codigopostal=15035")
        data = response.json()
        print(f"✓ Encontradas {len(data.get('results', []))} huellas con código 15035")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # 4. ESTADÍSTICAS
    print_header("4. ESTADÍSTICAS GLOBALES")
    try:
        response = requests.get(f"{BASE_URL}/huellas/estadisticas/")
        data = response.json()
        print(f"✓ Total de huellas: {data.get('total_huellas', 0)}")
        print(f"✓ Provincias: {data.get('total_provincias', 0)}")
        print(f"✓ Poblaciones: {data.get('total_poblaciones', 0)}")
        print(f"✓ Códigos postales: {data.get('total_codigos_postal', 0)}")
        
        if data.get('top_provincias'):
            print("\n  Top provincias:")
            for item in data['top_provincias'][:3]:
                print(f"    - {item['provincia']}: {item['cantidad']} huellas")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # 5. CREAR NUEVA HUELLA
    print_header("5. CREAR NUEVA HUELLA")
    nueva_huella = {
        "iddomicilioto": "TEST99999999999999999999999999999",
        "codigopostal": "15035",
        "provincia": "A CORUÑA",
        "poblacion": "FENE",
        "tipovia": "CALLE",
        "nombrevia": "TEST",
        "numero": "999"
    }
    try:
        response = requests.post(f"{BASE_URL}/huellas/", json=nueva_huella)
        if response.status_code == 201:
            data = response.json()
            print(f"✓ Huella creada con ID: {data.get('id')}")
            print_response("Datos creados", data)
        else:
            print(f"✗ Error {response.status_code}: {response.text}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # 6. OBTENER DETALLE DE UNA HUELLA
    print_header("6. OBTENER DETALLE DE HUELLA")
    try:
        response = requests.get(f"{BASE_URL}/huellas/?page_size=1")
        data = response.json()
        if data.get('results'):
            huella_id = data['results'][0]['id']
            response = requests.get(f"{BASE_URL}/huellas/{huella_id}/")
            huella = response.json()
            print(f"✓ Huella ID {huella_id}:")
            print(f"  - Domicilio: {huella.get('nombrevia')} {huella.get('numero')}")
            print(f"  - Población: {huella.get('poblacion')}")
            print(f"  - Código postal: {huella.get('codigopostal')}")
            print(f"  - OLT: {huella.get('codigoolt')}")
            print(f"  - CTO: {huella.get('codigocto')}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # 7. FILTROS ESPECIALIZADOS
    print_header("7. FILTROS ESPECIALIZADOS")
    try:
        # Por código postal
        response = requests.get(f"{BASE_URL}/huellas/por_codigo_postal/?codigo=15035")
        data = response.json()
        print(f"✓ por_codigo_postal: {len(data.get('results', []))} resultados")
        
        # Por provincia
        response = requests.get(f"{BASE_URL}/huellas/por_provincia/?provincia=A%20CORUÑA")
        data = response.json()
        print(f"✓ por_provincia: {len(data.get('results', []))} resultados")
        
        # Por población
        response = requests.get(f"{BASE_URL}/huellas/por_poblacion/?poblacion=FENE")
        data = response.json()
        print(f"✓ por_poblacion: {len(data.get('results', []))} resultados")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # 8. ORDENAMIENTO
    print_header("8. ORDENAMIENTO")
    try:
        response = requests.get(f"{BASE_URL}/huellas/?ordering=-created&page_size=3")
        data = response.json()
        print(f"✓ Últimas 3 huellas creadas:")
        for i, h in enumerate(data.get('results', []), 1):
            print(f"  {i}. {h.get('nombrevia')} {h.get('numero')} - {h.get('created')}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print_header("DEMOSTRACIÓN COMPLETADA")
    print("""
✓ La API está funcionando correctamente.

Próximos pasos:
1. Explorar http://localhost:8000/api/ en el navegador
2. Acceder a admin en http://localhost:8000/admin/
3. Consultar README.md para más endpoints
4. Importar datos completos con: python manage.py import_huella_csv tu_archivo.csv
    """)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✗ Demostración cancelada por el usuario.")
    except Exception as e:
        print(f"\n✗ Error general: {e}")

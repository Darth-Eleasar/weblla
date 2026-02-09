#!/usr/bin/env python
"""
Script para iniciar el servidor Django e importar CSV automáticamente
Ejecutar: python run_server.py
"""
import os
import sys
import subprocess
import django
from pathlib import Path

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'huella_project.settings')
django.setup()

from django.core.management import call_command
from huella_app.models import Huella

def main():
    print("\n" + "="*60)
    print("🚀 HUELLA APP - INICIO DEL SERVIDOR")
    print("="*60 + "\n")
    
    # 1. Realizar migraciones
    print("📦 Aplicando migraciones...")
    call_command('migrate')
    print("✓ Migraciones completadas\n")
    
    # 2. Contar huellas existentes
    count_before = Huella.objects.count()
    print(f"📊 Huellas existentes en BD: {count_before}\n")
    
    # 3. Importar CSV si existe y la BD está vacía
    csv_path = Path(__file__).parent / 'datos_ch.csv'
    
    if not csv_path.exists():
        csv_path = Path(__file__).parent / 'ejemplo_datos.csv'
    
    if csv_path.exists():
        print(f"📥 Importando datos desde: {csv_path}")
        try:
            call_command('import_huella_csv', str(csv_path), '--skip-errors')
            count_after = Huella.objects.count()
            print(f"✓ Importación completada. Total huellas: {count_after}\n")
        except Exception as e:
            print(f"⚠️  Error en importación: {e}\n")
    else:
        print(f"⚠️  CSV no encontrado en: {csv_path}\n")
    
    # 4. Mostrar información del servidor
    print("="*60)
    print("✅ SERVIDOR LISTO")
    print("="*60)
    print("\n📍 Backend:  http://localhost:8000")
    print("📍 API:      http://localhost:8000/api/huellas/")
    print("📍 Admin:    http://localhost:8000/admin/")
    print("📍 Frontend: http://localhost:5173 (en otra terminal: npm run dev)\n")
    print("Presiona CTRL+C para detener\n")
    
    # 5. Iniciar servidor
    call_command('runserver', '0.0.0.0:8000')

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Servidor detenido")
        sys.exit(0)

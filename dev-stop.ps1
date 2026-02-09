Write-Host "==================================" -ForegroundColor Cyan
Write-Host "  Deteniendo entorno de desarrollo" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

$PidFile = Join-Path $PSScriptRoot ".dev_pids"

Write-Host "[1/3] Cerrando ventanas de Django, Celery y React..." -ForegroundColor Yellow

if (Test-Path $PidFile) {
    $pids = Get-Content $PidFile
    foreach ($id in $pids) {
        if ($id) {
            # /F = Fuerza bruta
            # /T = Cierra tambien los procesos hijos (Python, Node, etc)
            # /PID = El ID del proceso
            taskkill /F /T /PID $id 2>$null
        }
    }
    Remove-Item $PidFile -ErrorAction SilentlyContinue
    Write-Host "✓ Ventanas cerradas" -ForegroundColor Green
} else {
    Write-Host "! No se encontro el archivo .dev_pids. Intentando cierre por nombre..." -ForegroundColor Yellow
    
    # Fallback: Cerramos procesos por nombre
    $djangoProcesses = Get-Process python -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like "*manage.py*runserver*" }
    $celeryProcesses = Get-Process python -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like "*celery*" }
    $reactProcesses = Get-Process node -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like "*vite*" }

    if ($djangoProcesses) {
        $djangoProcesses | Stop-Process -Force
        Write-Host "✓ Django detenido" -ForegroundColor Green
    } else {
        Write-Host "  Django no estaba corriendo" -ForegroundColor Gray
    }

    if ($celeryProcesses) {
        $celeryProcesses | Stop-Process -Force
        Write-Host "✓ Celery detenido" -ForegroundColor Green
    } else {
        Write-Host "  Celery no estaba corriendo" -ForegroundColor Gray
    }

    if ($reactProcesses) {
        $reactProcesses | Stop-Process -Force
        Write-Host "✓ React detenido" -ForegroundColor Green
    } else {
        Write-Host "  React no estaba corriendo" -ForegroundColor Gray
    }
}

Write-Host ""
Write-Host "[2/3] Deteniendo PostgreSQL y Redis (Docker)..." -ForegroundColor Yellow
& docker compose -f docker-compose.dev.yml down

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ PostgreSQL y Redis detenidos correctamente" -ForegroundColor Green
} else {
    Write-Host "✗ Error al detener los contenedores Docker" -ForegroundColor Red
}

Write-Host ""
Write-Host "[3/3] Limpiando procesos residuales..." -ForegroundColor Yellow
# Limpiar cualquier proceso celery que haya quedado huerfano
Get-Process python -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like "*celery*" } | Stop-Process -Force -ErrorAction SilentlyContinue
Write-Host "✓ Limpieza completada" -ForegroundColor Green

Write-Host ""
Write-Host "===================================" -ForegroundColor Cyan
Write-Host "  Entorno detenido completamente" -ForegroundColor Cyan
Write-Host "===================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Presiona cualquier tecla para cerrar..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
# Primero, limpiamos la consola para evitar ruido de errores previos
Clear-Host

# Definimos la ruta del archivo de IDs
$PidFile = Join-Path $PSScriptRoot ".dev_pids"

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "  Iniciando entorno de desarrollo" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan

Write-Host ""
Write-Host "[1/6] Levantando PostgreSQL y Redis..." -ForegroundColor Yellow
& docker compose -f docker-compose.dev.yml up -d

if ($LASTEXITCODE -ne 0) 
{
    Write-Host "✗ Error al iniciar Docker" -ForegroundColor Red
    exit 1
}
Write-Host "✓ PostgreSQL y Redis iniciados" -ForegroundColor Green

Write-Host ""
Write-Host "[2/6] Esperando a que los servicios esten listos..." -ForegroundColor Yellow
Start-Sleep -Seconds 5
Write-Host "✓ Servicios Docker listos" -ForegroundColor Green

Write-Host ""
Write-Host "[3/6] Iniciando servidor backend (Django)..." -ForegroundColor Yellow

# Definimos la ruta del ejecutable de python dentro del venv
$PythonVenv = ""
if (Test-Path "$pwd\venv\Scripts\python.exe") { 
    $PythonVenv = "$pwd\venv\Scripts\python.exe" 
}
elseif (Test-Path "$pwd\.venv\Scripts\python.exe") { 
    $PythonVenv = "$pwd\.venv\Scripts\python.exe" 
}

if ($PythonVenv -eq "") {
    Write-Host "! No se encontro el entorno virtual en \venv o \.venv" -ForegroundColor Red
    exit 1
}

$BackendCmd = "cd backend; `$env:DJANGO_SETTINGS_MODULE='huella_project.settings_local'; & '$PythonVenv' manage.py runserver"
$procBackend = Start-Process powershell -ArgumentList "-NoExit", "-Command", $BackendCmd -PassThru
Write-Host "✓ Backend configurado para usar: $PythonVenv" -ForegroundColor Green

Write-Host ""
Write-Host "[4/6] Esperando a que Django este listo..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

Write-Host ""
Write-Host "[5/6] Iniciando Celery Worker..." -ForegroundColor Yellow

$CeleryCmd = "cd backend; `$env:DJANGO_SETTINGS_MODULE='huella_project.settings_local'; & '$PythonVenv' -m celery -A huella_project worker --loglevel=info --pool=solo"
$procCelery = Start-Process powershell -ArgumentList "-NoExit", "-Command", $CeleryCmd -PassThru
Write-Host "✓ Celery Worker iniciado" -ForegroundColor Green

Write-Host ""
Write-Host "[6/6] Iniciando servidor frontend (React)..." -ForegroundColor Yellow

$FrontendCmd = "cd frontend; `$env:VITE_BACKEND_URL='http://localhost:8000'; npm run dev"
$procFrontend = Start-Process powershell -ArgumentList "-NoExit", "-Command", $FrontendCmd -PassThru
Write-Host "✓ Frontend iniciado apuntando a localhost:8000" -ForegroundColor Green

Write-Host ""
Write-Host "===================================" -ForegroundColor Cyan
Write-Host "  Entorno iniciado correctamente" -ForegroundColor Cyan
Write-Host "===================================" -ForegroundColor Cyan

# Guardamos los IDs en un archivo para el script de parada
$procBackend.Id, $procCelery.Id, $procFrontend.Id | Out-File $PidFile

Write-Host "✓ Procesos registrados (Backend: $($procBackend.Id), Celery: $($procCelery.Id), Frontend: $($procFrontend.Id))" -ForegroundColor Green
Write-Host ""
Write-Host "Servicios activos:" -ForegroundColor White
Write-Host "  PostgreSQL: localhost:5432 (Docker)" -ForegroundColor Cyan
Write-Host "  Redis:      localhost:6379 (Docker)" -ForegroundColor Cyan
Write-Host "  Backend:    http://localhost:8000 (Local)" -ForegroundColor Cyan
Write-Host "  Celery:     Worker activo (Local)" -ForegroundColor Cyan
Write-Host "  Frontend:   http://localhost:5173 (Local)" -ForegroundColor Cyan
Write-Host ""
Write-Host "Para detener: ejecuta .\dev-stop.ps1" -ForegroundColor Yellow
Write-Host ""
Write-Host "Presiona cualquier tecla para cerrar esta ventana..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
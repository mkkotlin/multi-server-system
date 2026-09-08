# Multi-Server System Startup Script for PowerShell

Write-Host "Starting Django..." -ForegroundColor Cyan
$django = Start-Process -FilePath ".\services\Django\environment\Scripts\python.exe" -ArgumentList "manage.py runserver" -WorkingDirectory ".\services\Django" -PassThru

Write-Host "Starting Node..." -ForegroundColor Green
$node = Start-Process -FilePath "npm.cmd" -ArgumentList "run dev" -WorkingDirectory ".\services\Node" -PassThru

if (Test-Path ".\services\FastAPI\app\main.py") {
    Write-Host "Starting FastAPI..." -ForegroundColor Yellow
    $fastapi = Start-Process -FilePath ".\services\FastAPI\fastAPIenv\Scripts\python.exe" -ArgumentList "-m uvicorn app.main:app --port 8002 --reload" -WorkingDirectory ".\services\FastAPI" -PassThru
} elseif (Test-Path ".\services\FastAPI\main.py") {
    Write-Host "Starting FastAPI..." -ForegroundColor Yellow
    $fastapi = Start-Process -FilePath ".\services\FastAPI\fastAPIenv\Scripts\python.exe" -ArgumentList "-m uvicorn main:app --port 8002 --reload" -WorkingDirectory ".\services\FastAPI" -PassThru
} else {
    Write-Host "Notice: FastAPI app/main.py not found. Skipping FastAPI server." -ForegroundColor Yellow
}

Write-Host "`nAll services started! Press Ctrl+C in this window to stop all services." -ForegroundColor Magenta

try {
    while ($true) {
        Start-Sleep -Seconds 1
    }
} finally {
    Write-Host "`nStopping services..." -ForegroundColor Red
    if ($django -and -not $django.HasExited) { Stop-Process -Id $django.Id -Force -ErrorAction SilentlyContinue }
    if ($node -and -not $node.HasExited) { Stop-Process -Id $node.Id -Force -ErrorAction SilentlyContinue }
    if ($fastapi -and -not $fastapi.HasExited) { Stop-Process -Id $fastapi.Id -Force -ErrorAction SilentlyContinue }
}

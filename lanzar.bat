@echo off
setlocal enabledelayedexpansion

REM === 1) Ir a la carpeta del proyecto ===
cd /d "%~dp0"

echo ================================
echo  Lanzador Comandas con uv (Win)
echo ================================
echo.

REM === 2) Verificar 'uv' ===
where uv >nul 2>nul
if errorlevel 1 (
  echo ❌ No encuentro 'uv' en el PATH. Instalalo y reintenta.
  pause
  exit /b 1
)

REM === 3) Sincronizar dependencias (opcional pero util) ===
echo 🔄 uv sync...
uv sync

REM === 4) Levantar el servidor en una ventana aparte (no bloquea este .bat)
echo 🚀 Iniciando servidor Django en nueva ventana...
start "Servidor Comandas (Django)" cmd /k "cd /d %~dp0 && uv run python manage.py runserver 0.0.0.0:8000"

REM === 5) Esperar a que el puerto 8000 esté escuchando antes de abrir el navegador ===
echo ⏳ Esperando a que el servidor este listo en http://127.0.0.1:8000 ...
powershell -NoProfile -Command ^
  "$p=8000; while ($true) { $ok=$false; try { $c=New-Object Net.Sockets.TcpClient; $c.Connect('127.0.0.1',$p); if($c.Connected){$ok=$true}; $c.Close() } catch {} ; if($ok){ break } ; Start-Sleep -Milliseconds 400 }"

REM === 6) Abrir pestañas en el navegador predeterminado (agrega o quita las que quieras)
start "" "http://127.0.0.1:8000/"
start "" "http://127.0.0.1:8000/pedidos_pendientes/"

echo ✅ Listo. Dejé el servidor corriendo en otra ventana.
echo    Cierra esta solo si no la necesitas.


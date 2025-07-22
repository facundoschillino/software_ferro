import subprocess
import sys
import os
import webbrowser

# Ruta absoluta al entorno virtual
venv_python = os.path.abspath("venv/Scripts/python.exe")

# Verificamos que el ejecutable existe
if not os.path.exists(venv_python):
    print("No se encontró el entorno virtual en 'venv/Scripts/python.exe'")
    sys.exit(1)

# Comando para levantar el servidor
server_cmd = [venv_python, "manage.py", "runserver"]

# Abrir dos ventanas del navegador
webbrowser.open_new("http://127.0.0.1:8000")  # Página principal
webbrowser.open_new("http://127.0.0.1:8000/pedidos_pendientes")  # Página secundaria

# Ejecutar servidor
subprocess.run(server_cmd)

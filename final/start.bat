@echo off
type nul > logs.txt
start cmd /k "python Kernel.py"
timeout /t 1
start cmd /k "python GestorArchivos.py"
timeout /t 1
start cmd /k "python Aplicacion.py"
timeout /t 1
start cmd /k "python Interfaz.py"


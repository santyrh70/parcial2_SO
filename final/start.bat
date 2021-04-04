@echo off
type nul > logs.txt
start cmd /k "python Kernel.py" ^&^& exit
timeout /t 1
start cmd /k "python GestorArchivos.py" ^&^& exit
timeout /t 1
start cmd /k "python Aplicacion.py" ^&^& exit
timeout /t 1
start cmd /k "python Interfaz.py" ^&^& exit
exit

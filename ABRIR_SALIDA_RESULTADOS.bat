@echo off
cd /d "%~dp0"
if not exist "salida_resultados" (
    echo No existe la carpeta salida_resultados.
    echo Ejecuta primero el proyecto en NetBeans y elige la opcion 1 o 2.
    pause
    exit /b
)
start "" "salida_resultados"

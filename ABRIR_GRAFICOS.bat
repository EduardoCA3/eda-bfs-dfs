@echo off
cd /d "%~dp0"
if not exist "salida_resultados" (
    echo No existe la carpeta salida_resultados.
    echo Ejecuta primero el proyecto en NetBeans y elige la opcion 1 o 2.
    pause
    exit /b
)
if exist "salida_resultados\animacion_grafos.html" (
    start "" "salida_resultados\animacion_grafos.html"
)
if exist "salida_resultados\dashboard_prueba_simple.html" (
    start "" "salida_resultados\dashboard_prueba_simple.html"
)
if exist "salida_resultados\dashboard_resultados.html" (
    start "" "salida_resultados\dashboard_resultados.html"
)
if exist "salida_resultados\animacion_opcion2.html" (
    start "" "salida_resultados\animacion_opcion2.html"
)
if not exist "salida_resultados\animacion_grafos.html" if not exist "salida_resultados\dashboard_prueba_simple.html" if not exist "salida_resultados\dashboard_resultados.html" if not exist "salida_resultados\animacion_opcion2.html" (
    echo Todavia no hay graficos HTML.
    echo Ejecuta primero la opcion 1 o la opcion 2 desde NetBeans.
    pause
)

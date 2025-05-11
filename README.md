# NT_Group

> Crear virtualizacion de python

py -m venv env

> Activar virtualizacion usando powershell

.\env\Scripts\activate  (nota: se debe de ubicar en la misma carpeta del repositorio)

> Se valida que exista el archivo de requirements

pip freeze .\requirements.txt 

> Instalacion de librerias necesarias

pip install -r .\requirements.txt



> Ejecucion API, se debe de estar en la carpeta seccion_2

uvicorn main:app --port 6660 --reload

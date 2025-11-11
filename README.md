# Evaluación Taller

Este proyecto forma parte de la Evaluación del Taller de Programación.

---

## 🧰 Requerimientos de instalación

1. Clonar el repositorio
```bash
git clone https://github.com/Dania2701/Evaluacion_Taller.git
cd Evaluacion_Taller/reportes_hoyos

python -m venv venv
venv\Scripts\activate

pip install -r [requirements.txt](http://_vscodecontentref_/0)

python manage.py runserver


Comandos PowerShell para escribir ambos archivos (ejecutar en Windows PowerShell):
```powershell
# Crear/actualizar requirements.txt
@"
asgiref==3.10.0
Django==5.2.8
sqlparse==0.5.3
tzdata==2025.2
django-crispy-tailwind>=0.5
"@ | Set-Content -Path "C:\Users\dania\Desktop\Evaluacion_3_taller\requirements.txt" -Encoding utf8

# Crear/actualizar README.md
@"
# Evaluación Taller

Este proyecto forma parte de la Evaluación del Taller de Programación.

---

## 🧰 Requerimientos de instalación

1. Clonar el repositorio
```bash
git clone https://github.com/Dania2701/Evaluacion_Taller.git
cd Evaluacion_Taller/reportes_hoyos

2. Crear y activar entorno virtual (Windows)
python -m venv venv
venv\Scripts\activate

3. Instalar dependencias
pip install django

4. Ejecutar servidor de desarrollo
python manage.py runserver
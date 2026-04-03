"""
setup_proyecto.py
-----------------
Corre este script UNA SOLA VEZ después de clonar el repositorio.
Crea todas las carpetas necesarias y verifica que el ambiente esté listo.

Uso:
    python setup_proyecto.py
"""

import os
import sys
from pathlib import Path

# ── Estructura de carpetas ────────────────────────────────────────────────────

CARPETAS = [
    # Datos crudos — organizados por fuente y año
    "datos/raw/geih/2023/enero",
    "datos/raw/geih/2023/febrero",
    "datos/raw/geih/2023/marzo",
    "datos/raw/geih/2023/abril",
    "datos/raw/geih/2023/mayo",
    "datos/raw/geih/2023/junio",
    "datos/raw/geih/2023/julio",
    "datos/raw/geih/2023/agosto",
    "datos/raw/geih/2023/septiembre",
    "datos/raw/geih/2023/octubre",
    "datos/raw/geih/2023/noviembre",
    "datos/raw/geih/2023/diciembre",
    # Datos procesados
    "datos/processed",
    "datos/diccionarios",
    # Pipelines ETL
    "pipelines/geih",
    # Análisis
    "analisis/geih_mercado_laboral",
    # Reportes generados
    "reportes",
    # GitHub Actions
    ".github/workflows",
]

GITKEEP_EN = [
    "datos/raw/geih/2023/enero",
    "datos/processed",
    "datos/diccionarios",
    "reportes",
]


def crear_estructura():
    print("\n📁 Creando estructura de carpetas...\n")
    raiz = Path(".")

    for carpeta in CARPETAS:
        ruta = raiz / carpeta
        ruta.mkdir(parents=True, exist_ok=True)
        print(f"   ✓ {carpeta}")

    # Archivos .gitkeep para que Git rastree carpetas vacías
    for carpeta in GITKEEP_EN:
        gitkeep = raiz / carpeta / ".gitkeep"
        gitkeep.touch()

    print("\n✅ Estructura creada.\n")


def crear_gitignore():
    contenido = """# Python
__pycache__/
*.py[cod]
*.pyo
.venv/
env/
*.egg-info/
dist/
build/

# Jupyter
.ipynb_checkpoints/
*.ipynb_checkpoints

# Datos crudos (no subir al repositorio — son pesados)
datos/raw/

# Variables de entorno
.env

# IDEs
.vscode/
.idea/
*.DS_Store

# Quarto
/_site/
/.quarto/
"""
    with open(".gitignore", "w") as f:
        f.write(contenido)
    print("✅ .gitignore creado.")


def crear_env_ejemplo():
    contenido = """# Copia este archivo como .env y completa tus valores
# NUNCA subas .env al repositorio

# Rutas (opcional, por defecto usa rutas relativas)
RUTA_DATOS_RAW=datos/raw
RUTA_DATOS_PROCESADOS=datos/processed
"""
    with open(".env.ejemplo", "w") as f:
        f.write(contenido)
    print("✅ .env.ejemplo creado.")


def verificar_python():
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print(f"⚠️  Python {version.major}.{version.minor} detectado.")
        print("   Se recomienda Python 3.10 o superior.")
    else:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} — OK")


def verificar_dependencias():
    paquetes = ["pandas", "numpy", "pyarrow", "duckdb", "requests", "plotly"]
    print("\n📦 Verificando dependencias clave...\n")
    faltantes = []
    for pkg in paquetes:
        try:
            __import__(pkg)
            print(f"   ✓ {pkg}")
        except ImportError:
            print(f"   ✗ {pkg} — NO instalado")
            faltantes.append(pkg)

    if faltantes:
        print(f"\n⚠️  Instala los faltantes con:")
        print(f"   pip install {' '.join(faltantes)}\n")
    else:
        print("\n✅ Todas las dependencias clave están instaladas.\n")


def resumen_final():
    print("=" * 55)
    print("  PROYECTO LISTO — Próximos pasos:")
    print("=" * 55)
    print("""
  1. git init  (si no has iniciado el repositorio)
  2. git add .
  3. git commit -m "feat: estructura inicial del proyecto"
  4. Crear repositorio en github.com y hacer push

  Luego continúa con la Etapa 1:
  → Descargar microdatos GEIH 2023 desde:
    https://microdatos.dane.gov.co
""")


if __name__ == "__main__":
    verificar_python()
    crear_estructura()
    crear_gitignore()
    crear_env_ejemplo()
    verificar_dependencias()
    resumen_final()

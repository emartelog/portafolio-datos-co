# Portafolio de Ciencia de Datos — Colombia

Análisis estadísticos automatizados sobre temas económicos y sociales usando datos de fuentes oficiales colombianas (DANE, XM, Policía Nacional, Banco de la República).

**Autor:** [Tu nombre]  
**Contacto:** [Tu correo]  
**Sitio web:** [tu-usuario.github.io/portafolio-datos-co]

---

## Objetivo

Este repositorio construye y mantiene un portafolio profesional de análisis de datos con tres propósitos:

1. **Contratos con el Estado:** Demostrar capacidad analítica para propuestas a entidades públicas (gobernaciones, DNP, DANE, alcaldías).
2. **Perfil docente universitario:** Evidenciar producción académica y manejo de microdatos oficiales.
3. **Investigación en Colciencias/MinCiencias:** Base para publicación de papers en revistas indexadas.

---

## Estructura del repositorio

```
portafolio-datos-co/
├── .github/
│   └── workflows/              # Pipelines automáticos (GitHub Actions)
├── datos/
│   ├── raw/                    # Datos originales sin modificar (nunca tocar)
│   │   └── geih/
│   │       └── 2023/           # Un directorio por año
│   │           ├── enero/
│   │           ├── febrero/
│   │           └── ...
│   ├── processed/              # Datos limpios en formato Parquet
│   └── diccionarios/           # Documentación de variables por fuente
├── pipelines/
│   └── geih/                   # Scripts ETL de la GEIH
│       ├── descarga.py         # Descarga automática desde DANE
│       ├── etl_2023.py         # Limpieza y transformación
│       └── variables.py        # Construcción de indicadores derivados
├── analisis/
│   └── geih_mercado_laboral/   # Primer análisis: mercado laboral región Caribe
│       ├── notebook.ipynb      # Análisis exploratorio
│       └── reporte.qmd         # Reporte Quarto para publicación
├── reportes/                   # Salidas HTML/PDF generadas automáticamente
├── requirements.txt            # Dependencias Python
├── environment.yml             # Ambiente Conda (alternativa)
└── README.md                   # Este archivo
```

---

## Fuentes de datos

| Fuente | Descripción | Frecuencia | Estado |
|--------|-------------|------------|--------|
| DANE — GEIH | Gran Encuesta Integrada de Hogares | Mensual | ✅ Activo |
| XM | Datos del mercado eléctrico colombiano | Diario/Mensual | 🔜 Próximamente |
| Policía Nacional | Estadísticas delictivas | Mensual | 🔜 Próximamente |
| Banco de la República | Indicadores macroeconómicos | Variable | 🔜 Próximamente |

---

## Análisis publicados

### 1. Mercado laboral en la región Caribe (2023)
**Fuente:** DANE — GEIH 2023  
**Metodología:** Estadística descriptiva, brechas de género, regresión logística  
**Pregunta:** ¿Qué factores determinan la probabilidad de empleo formal en la región Caribe colombiana?  
**Estado:** 🔄 En construcción

---

## Cómo reproducir los análisis

### Requisitos
- Python 3.10+
- Git

### Instalación

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/portafolio-datos-co.git
cd portafolio-datos-co

# Crear ambiente virtual
python -m venv .venv
source .venv/bin/activate       # Linux/Mac
.venv\Scripts\activate          # Windows

# Instalar dependencias
pip install -r requirements.txt
```

### Descargar y procesar datos

```bash
# Descargar microdatos GEIH 2023
python pipelines/geih/descarga.py --year 2023

# Correr pipeline ETL
python pipelines/geih/etl_2023.py
```

### Ejecutar análisis

```bash
# Abrir Jupyter
jupyter lab analisis/geih_mercado_laboral/notebook.ipynb

# Renderizar reporte Quarto
quarto render analisis/geih_mercado_laboral/reporte.qmd
```

---

## Publicaciones y papers

| Título | Revista objetivo | Estado |
|--------|-----------------|--------|
| Determinantes del empleo formal en la Costa Caribe colombiana: evidencia de la GEIH 2023 | Lecturas de Economía (U de A) | 🔄 En preparación |

---

## Licencia

Los análisis y código de este repositorio están bajo licencia MIT. Los datos son de fuentes públicas oficiales y su uso sigue los términos de cada entidad.

---

*Última actualización automática: ver historial de commits*

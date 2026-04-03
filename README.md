# Portafolio de Ciencia de Datos — Colombia

Análisis estadísticos automatizados sobre temas económicos y sociales usando datos de fuentes oficiales colombianas (DANE, XM, Policía Nacional, Banco de la República).

**Autor:** Efrain Martelo Gomez  
**Contacto:** efrainmartelo@gmail.com  
**Sitio web:** [emartelog.github.io/portafolio-datos-co]

---

## Objetivo

Producir análisis cuantitativos de alta calidad sobre las brechas 
socioeconómicas de Colombia — con énfasis en la región Caribe — 
a partir de fuentes oficiales como el DANE, XM y la Policía Nacional. 
Los análisis son automatizados, reproducibles y se actualizan 
continuamente, generando conocimiento accionable para la toma de 
decisiones en política pública local y regional.

### Líneas de trabajo

1. **Mercado laboral y brechas sociales:** Desempleo, informalidad, 
   género y juventud desde microdatos GEIH. Insumo directo para 
   propuestas a gobernaciones, alcaldías y el DNP.

2. **Producción académica indexada:** Cada análisis es base de un 
   paper para revistas Publindex A1/A2 (Lecturas de Economía, 
   Sociedad y Economía, Cuadernos de Economía).

3. **Capacidad instalada para el Estado:** Demostrar que el análisis 
   automatizado de fuentes oficiales puede apoyar decisiones de 
   política pública con metodología transparente y costo eficiente.
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

### 1. Mercado laboral en la región Caribe (2024-2025)
**Fuente:** DANE — GEIH 2024-2025  
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

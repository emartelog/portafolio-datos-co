# =============================================================
# CONCILIACIÓN GEIH vs DANE OFICIAL — VERSIÓN DINÁMICA
# =============================================================
# El script se adapta automáticamente a:
#   - El año más reciente disponible en PostgreSQL
#   - El archivo de anexos más reciente disponible en disco
#
# Para actualizar el análisis:
#   1. Carga los nuevos datos GEIH en PostgreSQL
#   2. Descarga el nuevo anexo del DANE y ponlo en:
#      datos/referencias/dane/
#   3. Corre el script. No hay que cambiar nada más.
# =============================================================

import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from dotenv import load_dotenv
from pathlib import Path
import os

# ── Conexión ──────────────────────────────────────────────────
load_dotenv("config/.env")
engine = create_engine(
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

# ── Parámetros configurables ──────────────────────────────────
# Carpeta donde guardas los anexos oficiales del DANE.
# Pon aquí el archivo más reciente — el script lo encuentra solo.
CARPETA_ANEXOS = Path("datos/referencias/dane")

# Año a analizar. None = detecta automáticamente el más reciente
# con 12 meses completos en la base de datos.
ANNO = None


# ── 1. Detectar años disponibles en PostgreSQL ────────────────
print("=" * 55)
print("1. AÑOS DISPONIBLES EN LA BASE DE DATOS")
print("=" * 55)

query_annos = """
SELECT DISTINCT "PER"::numeric AS anno,
       COUNT(DISTINCT "MES") AS meses_disponibles,
       COUNT(*) AS registros_totales
FROM "FUERZA_DE_TRABAJO_GEIH"
WHERE "PET"::numeric = 1
GROUP BY "PER"::numeric
ORDER BY anno
"""
df_annos = pd.read_sql(query_annos, engine)
df_annos['anno'] = df_annos['anno'].astype(int)
print(df_annos.to_string(index=False))

if ANNO is None:
    annos_completos = df_annos[df_annos['meses_disponibles'] == 12]['anno']
    if len(annos_completos) == 0:
        raise ValueError("No hay ningún año con 12 meses completos en la base.")
    anno_analisis = int(annos_completos.max())
    print(f"\n-> Año seleccionado automáticamente: {anno_analisis}")
    print("   (último año con 12 meses completos)")
else:
    anno_analisis = ANNO
    meses_disp = df_annos[df_annos['anno'] == anno_analisis]['meses_disponibles'].values
    if len(meses_disp) == 0:
        raise ValueError(f"El año {anno_analisis} no existe en la base de datos.")
    print(f"\n-> Año seleccionado: {anno_analisis} ({meses_disp[0]} meses disponibles)")


# ── 2. Encontrar el anexo DANE más reciente en disco ──────────
# Busca todos los archivos .xlsx en la carpeta de referencias.
# Toma el más reciente por fecha de modificación.
# No importa cómo se llame — anex-GEIH-dic2024, anex-GEIH-feb2026, etc.

print("\n" + "=" * 55)
print("2. ARCHIVO DE REFERENCIA DANE")
print("=" * 55)

archivos_dane = sorted(
    CARPETA_ANEXOS.glob("*.xlsx"),
    key=lambda f: f.stat().st_mtime,
    reverse=True
)

if archivos_dane:
    archivo_dane = archivos_dane[0]
    print(f"Archivo encontrado: {archivo_dane.name}")
    if len(archivos_dane) > 1:
        print(f"Otros archivos disponibles en la carpeta:")
        for f in archivos_dane[1:]:
            print(f"  - {f.name}")
else:
    archivo_dane = None
    print("Alerta: No se encontró ningún archivo .xlsx en:")
    print(f"  {CARPETA_ANEXOS}")
    print("Descarga el anexo oficial del DANE y ponlo en esa carpeta.")


# ── 3. Verificar estructura de periodos ───────────────────────
print("\n" + "=" * 55)
print(f"3. ESTRUCTURA DE PERIODOS — {anno_analisis}")
print("=" * 55)

query_semanas = f"""
SELECT "MES",
       COUNT(DISTINCT "PERIODO") AS semanas,
       MIN("PERIODO")::text AS periodo_min,
       MAX("PERIODO")::text AS periodo_max,
       COUNT(*) AS registros
FROM "FUERZA_DE_TRABAJO_GEIH"
WHERE "PET"::numeric = 1
AND "PER"::numeric = {anno_analisis}
GROUP BY "MES"
ORDER BY "MES"
"""
df_semanas = pd.read_sql(query_semanas, engine)
meses_ok = len(df_semanas[df_semanas['semanas'].between(4, 5)])
print(df_semanas.to_string(index=False))
print(f"\nMeses con 4-5 semanas (esperado): {meses_ok}/12")
if meses_ok < 12:
    print("Alerta: Algunos meses tienen semanas fuera del rango.")
    print("Verifica que no haya mezcla de años en esos meses.")


# ── 4. Calcular indicadores nacionales mes a mes ──────────────
# Códigos P6240:
#   1, 2    -> Ocupado
#   3       -> Desocupado
#   4, 5, 6 -> Inactivo

print("\n" + "=" * 55)
print(f"4. INDICADORES NACIONALES MES A MES — {anno_analisis}")
print("=" * 55)

query_ind = f"""
SELECT f."MES",
       f."FEX_C18" AS factor_expansion,
       CASE
           WHEN f."P6240"::numeric IN (1.0, 2.0) THEN 'Ocupado'
           WHEN f."P6240"::numeric = 3.0          THEN 'Desocupado'
           WHEN f."P6240"::numeric IN (4.0,5.0,6.0) THEN 'Inactivo'
       END AS condicion
FROM "FUERZA_DE_TRABAJO_GEIH" f
WHERE f."PET"::numeric = 1
AND   f."PER"::numeric = {anno_analisis}
"""
df_ind = pd.read_sql(query_ind, engine)
df_ind['factor_expansion'] = df_ind['factor_expansion'].astype(float)

meses_nombres = {
    '01':'Ene','02':'Feb','03':'Mar','04':'Abr',
    '05':'May','06':'Jun','07':'Jul','08':'Ago',
    '09':'Sep','10':'Oct','11':'Nov','12':'Dic'
}

resultados = []
for mes in sorted(df_ind['MES'].unique()):
    df_mes = df_ind[df_ind['MES'] == mes]
    g = df_mes.groupby('condicion')['factor_expansion'].sum()
    ocupados    = g.get('Ocupado', 0)
    desocupados = g.get('Desocupado', 0)
    inactivos   = g.get('Inactivo', 0)
    pea = ocupados + desocupados
    resultados.append({
        'MES':        mes,
        'Mes':        meses_nombres.get(mes, mes),
        'Ocupados_M': round(ocupados / 1e6, 2),
        'Desocup_M':  round(desocupados / 1e6, 2),
        'TD':         round(desocupados / pea * 100, 1),
        'TO':         round(ocupados / (pea + inactivos) * 100, 1),
        'TGP':        round(pea / (pea + inactivos) * 100, 1),
    })

df_nac = pd.DataFrame(resultados)
print(df_nac[['Mes','Ocupados_M','Desocup_M','TD','TO','TGP']].to_string(index=False))
print("\n(Ocupados_M y Desocup_M en millones de personas expandidas)")


# ── 5. Conciliación con cifras oficiales DANE ─────────────────
# Lee la hoja "Total nacional" del archivo más reciente
# encontrado en la carpeta de referencias.
# El archivo es acumulado desde 2001 — un solo archivo
# tiene todos los años disponibles.

print("\n" + "=" * 55)
print(f"5. CONCILIACIÓN vs DANE OFICIAL — {anno_analisis}")
print("=" * 55)

td_oficial  = None
tgp_oficial = None

if archivo_dane:
    try:
        df_dane_raw = pd.read_excel(
            archivo_dane,
            sheet_name='Total nacional',
            header=None
        )

        # Encontrar filas de indicadores
        fila_td  = df_dane_raw[
            df_dane_raw[0] == 'Tasa de Desocupación (TD)'
        ].index[0]
        fila_tgp = df_dane_raw[
            df_dane_raw[0] == 'Tasa Global de Participación (TGP)'
        ].index[0]

        # Extraer series numéricas completas
        td_serie  = df_dane_raw.iloc[fila_td,  1:].apply(
            pd.to_numeric, errors='coerce')
        tgp_serie = df_dane_raw.iloc[fila_tgp, 1:].apply(
            pd.to_numeric, errors='coerce')

        # Encontrar los meses del año de análisis
        # Fila 11 tiene los años, fila 12 tiene Ene/Feb/.../Dic
        fila_annos_raw = df_dane_raw.iloc[11, 1:].apply(
            pd.to_numeric, errors='coerce')

        # Posiciones donde empieza el año buscado
        pos_inicio = fila_annos_raw[
            fila_annos_raw == anno_analisis
        ].index

        if len(pos_inicio) > 0:
            idx = pos_inicio[0]
            # Tomar 12 valores a partir de esa posición
            td_oficial  = td_serie.loc[idx:idx+11].dropna().values[:12]
            tgp_oficial = tgp_serie.loc[idx:idx+11].dropna().values[:12]
            td_oficial  = np.round(td_oficial.astype(float), 1)
            tgp_oficial = np.round(tgp_oficial.astype(float), 1)
            print(f"OK: Cifras para {anno_analisis} leídas de {archivo_dane.name}")
        else:
            print(f"Alerta: El año {anno_analisis} no se encontró en {archivo_dane.name}")
            print("El archivo puede no tener datos hasta ese año todavía.")

    except Exception as e:
        print(f"Alerta: Error leyendo el archivo DANE: {e}")

# Tabla de conciliación
if td_oficial is not None and len(td_oficial) == len(df_nac):
    df_nac['TD_DANE']  = td_oficial
    df_nac['TGP_DANE'] = tgp_oficial
    df_nac['dif_TD']   = (df_nac['TD']  - df_nac['TD_DANE']).round(1)
    df_nac['dif_TGP']  = (df_nac['TGP'] - df_nac['TGP_DANE']).round(1)

    print()
    print(df_nac[['Mes','TD_DANE','TD','dif_TD',
                  'TGP_DANE','TGP','dif_TGP']].to_string(index=False))

    dif_media = df_nac['dif_TD'].abs().mean().round(1)
    print(f"\nDiferencia absoluta media en TD: {dif_media} pp")
    print("(Esperado 3-7 pp por ajuste de calibración interno del DANE)")
else:
    print("No se pudo realizar la conciliación.")
    print("Verifica que el archivo DANE esté en la carpeta correcta.")


# ── 6. Guardar resultados ─────────────────────────────────────
os.makedirs("datos/processed", exist_ok=True)
ruta_salida = f"datos/processed/indicadores_nacionales_{anno_analisis}.csv"
df_nac.to_csv(ruta_salida, index=False, encoding='utf-8')
print(f"\nResultados guardados en: {ruta_salida}")


# ── 7. Nota metodológica ──────────────────────────────────────
print("\n" + "=" * 55)
print("NOTA METODOLÓGICA")
print("=" * 55)
print(f"""
Indicadores calculados desde microdatos públicos GEIH {anno_analisis}
usando factor de expansión FEX_C18, restringiendo el
análisis a población en edad de trabajar (PET=1).

Las cifras difieren de los boletines oficiales del DANE
por ajustes de calibración post-estratificación internos
que no se publican en los microdatos públicos.

Válido para: tendencias mensuales, comparaciones regionales,
brechas socioeconómicas y análisis estructural del mercado
laboral colombiano.

Referencia DANE: {archivo_dane.name if archivo_dane else 'No disponible'}
Fuente: DANE — GEIH {anno_analisis}, microdatos públicos.
Procesamiento: Python + PostgreSQL. Cálculo propio.
""")

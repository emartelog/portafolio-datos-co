"""
verificar_raw.py
----------------
Verifica que los archivos crudos de la GEIH estén completos y bien organizados.
Corre esto después de descargar cada mes.

Uso:
    python pipelines/geih/verificar_raw.py
    python pipelines/geih/verificar_raw.py --year 2023 --mes enero
"""

import os
import argparse
from pathlib import Path

# ── Configuración ─────────────────────────────────────────────────────────────

RUTA_RAW = Path("datos/raw/geih")

MESES = [
    "enero", "febrero", "marzo", "abril",
    "mayo", "junio", "julio", "agosto",
    "septiembre", "octubre", "noviembre", "diciembre"
]

# Patrones que deben existir en cada mes (búsqueda parcial, no nombre exacto)
MODULOS_REQUERIDOS = [
    "características generales",
    "fuerza de trabajo",
    "ocupados",
    "desocupados",
    "inactivos",
]

# ── Funciones ─────────────────────────────────────────────────────────────────

def buscar_modulo(carpeta: Path, patron: str) -> Path | None:
    """Busca un archivo cuyo nombre contenga el patrón (sin distinción mayúsculas)."""
    for archivo in carpeta.iterdir():
        if archivo.suffix.lower() in (".csv", ".sav", ".dta"):
            if patron.lower() in archivo.name.lower():
                return archivo
    return None


def verificar_mes(year: str, mes: str) -> dict:
    """Verifica los archivos de un mes específico."""
    carpeta = RUTA_RAW / year / mes
    resultado = {
        "mes": mes,
        "carpeta_existe": carpeta.exists(),
        "modulos": {},
        "tiene_fuente_txt": False,
        "archivos_extra": [],
    }

    if not carpeta.exists():
        return resultado

    # Verificar módulos requeridos
    for modulo in MODULOS_REQUERIDOS:
        archivo = buscar_modulo(carpeta, modulo)
        if archivo:
            tamano_mb = archivo.stat().st_size / (1024 * 1024)
            resultado["modulos"][modulo] = {
                "encontrado": True,
                "archivo": archivo.name,
                "tamano_mb": round(tamano_mb, 2),
            }
        else:
            resultado["modulos"][modulo] = {"encontrado": False}

    # Verificar _fuente.txt
    resultado["tiene_fuente_txt"] = (carpeta / "_fuente.txt").exists()

    # Archivos que no corresponden a módulos conocidos
    for archivo in carpeta.iterdir():
        if archivo.name == "_fuente.txt":
            continue
        if archivo.suffix.lower() in (".csv", ".sav", ".dta"):
            es_conocido = any(
                m.lower() in archivo.name.lower()
                for m in MODULOS_REQUERIDOS
            )
            if not es_conocido:
                resultado["archivos_extra"].append(archivo.name)

    return resultado


def imprimir_resultado(resultado: dict):
    mes = resultado["mes"].capitalize()
    ok = "✅"
    warn = "⚠️ "
    err = "✗ "

    print(f"\n{'─'*50}")
    print(f"  {mes}")
    print(f"{'─'*50}")

    if not resultado["carpeta_existe"]:
        print(f"  {err} Carpeta no encontrada")
        return

    # Módulos
    todos_ok = True
    for modulo, info in resultado["modulos"].items():
        if info["encontrado"]:
            print(f"  {ok} {modulo:<35} {info['archivo'][:30]}  ({info['tamano_mb']} MB)")
        else:
            print(f"  {err} {modulo:<35} NO ENCONTRADO")
            todos_ok = False

    # _fuente.txt
    if resultado["tiene_fuente_txt"]:
        print(f"  {ok} _fuente.txt presente")
    else:
        print(f"  {warn} _fuente.txt ausente  (recomendado crearlo)")

    # Archivos extra (otros módulos del DANE)
    if resultado["archivos_extra"]:
        print(f"\n  Archivos adicionales encontrados:")
        for f in resultado["archivos_extra"]:
            print(f"    · {f}")

    if todos_ok:
        print(f"\n  → Mes completo ✅")
    else:
        print(f"\n  → Módulos faltantes — revisa la descarga ⚠️ ")


def resumen_general(year: str, resultados: list[dict]):
    completos = sum(
        1 for r in resultados
        if r["carpeta_existe"] and all(m["encontrado"] for m in r["modulos"].values())
    )
    print(f"\n{'='*50}")
    print(f"  Resumen GEIH {year}")
    print(f"{'='*50}")
    print(f"  Meses completos : {completos} / {len(resultados)}")
    print(f"  Meses faltantes : {len(resultados) - completos}")

    faltantes = [
        r["mes"] for r in resultados
        if not r["carpeta_existe"] or not all(m["encontrado"] for m in r["modulos"].values())
    ]
    if faltantes:
        print(f"\n  Descargar aún  : {', '.join(faltantes)}")
    else:
        print(f"\n  ✅ Todos los meses están listos para el ETL.")
    print()


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Verificar archivos raw GEIH")
    parser.add_argument("--year", default="2023", help="Año a verificar (default: 2023)")
    parser.add_argument("--mes", default=None, help="Mes específico a verificar (opcional)")
    args = parser.parse_args()

    print(f"\n🔍 Verificando GEIH {args.year} en: {RUTA_RAW / args.year}\n")

    if args.mes:
        resultado = verificar_mes(args.year, args.mes.lower())
        imprimir_resultado(resultado)
    else:
        resultados = []
        for mes in MESES:
            resultado = verificar_mes(args.year, mes)
            imprimir_resultado(resultado)
            resultados.append(resultado)
        resumen_general(args.year, resultados)


if __name__ == "__main__":
    main()

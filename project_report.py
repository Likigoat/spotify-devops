#!/usr/bin/env python3
"""
project_report.py
Genera un reporte de estado del proyecto SpotiDev.
Verifica que todos los archivos clave del proyecto existen.
"""

import os
import sys
from datetime import datetime

# ─── Configuración de colores ANSI ────────────────────────
class Colors:
    GREEN  = "\033[0;32m"
    RED    = "\033[0;31m"
    YELLOW = "\033[1;33m"
    CYAN   = "\033[0;36m"
    BLUE   = "\033[0;34m"
    BOLD   = "\033[1m"
    RESET  = "\033[0m"

def colored(text, color):
    """Aplica color al texto si el terminal lo soporta."""
    if sys.stdout.isatty():
        return f"{color}{text}{Colors.RESET}"
    return text

# ─── Archivos a verificar ─────────────────────────────────
FILES_TO_CHECK = [
    {
        "label": "Dockerfile app",
        "path":  "app/Dockerfile",
        "desc":  "Imagen del contenedor principal Flask"
    },
    {
        "label": "Dockerfile helper",
        "path":  "helper/Dockerfile",
        "desc":  "Imagen del servicio auxiliar"
    },
    {
        "label": "docker-compose.yml",
        "path":  "docker-compose.yml",
        "desc":  "Orquestación de contenedores"
    },
    {
        "label": "README.md",
        "path":  "README.md",
        "desc":  "Documentación del proyecto"
    },
    {
        "label": "infraestructura-base.yaml",
        "path":  "infraestructura-base.yaml",
        "desc":  "Plantilla CloudFormation para AWS"
    },
    {
        "label": "setup_project.sh",
        "path":  "setup_project.sh",
        "desc":  "Script de preparación del entorno"
    },
    {
        "label": "project_report.py",
        "path":  "project_report.py",
        "desc":  "Script de reporte (este archivo)"
    },
    {
        "label": "CI workflow (ci.yml)",
        "path":  ".github/workflows/ci.yml",
        "desc":  "Pipeline de GitHub Actions"
    },
]

# ─── Funciones de reporte ─────────────────────────────────

def print_separator(char="─", width=60):
    print(colored(char * width, Colors.CYAN))

def print_header():
    print()
    print_separator("═")
    print(colored("   🎵 SpotiDev – Reporte de Estado del Proyecto", Colors.BOLD))
    print_separator("═")
    print(f"   Fecha   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   Directorio: {os.path.abspath('.')}")
    print_separator("═")
    print()

def check_file(entry):
    """Verifica si un archivo existe y retorna su estado."""
    path = entry["path"]
    exists = os.path.isfile(path)
    return {
        "label": entry["label"],
        "path":  path,
        "desc":  entry["desc"],
        "found": exists,
        "size":  os.path.getsize(path) if exists else 0,
    }

def print_results(results):
    """Imprime los resultados del reporte."""
    found_count = 0

    print(colored("  Archivo                       Estado         Tamaño", Colors.BLUE))
    print_separator()

    for r in results:
        if r["found"]:
            status = colored("encontrado  ✔", Colors.GREEN)
            size   = colored(f"{r['size']:>6} bytes", Colors.CYAN)
            found_count += 1
        else:
            status = colored("no encontrado ✘", Colors.RED)
            size   = colored("       —", Colors.YELLOW)

        label_padded = r["label"].ljust(30)
        print(f"  {label_padded} {status:<25} {size}")

    return found_count

def print_summary(results, found_count):
    """Imprime el resumen del reporte."""
    total = len(results)
    missing = total - found_count

    print()
    print_separator()
    print(colored("  RESUMEN", Colors.BOLD))
    print_separator()
    print(f"  Total de archivos verificados : {total}")
    print(f"  Archivos encontrados          : {colored(str(found_count), Colors.GREEN)}")
    print(f"  Archivos faltantes            : {colored(str(missing), Colors.RED if missing > 0 else Colors.GREEN)}")
    print()

    if missing == 0:
        estado = colored("✅  Estado general: proyecto listo para validación", Colors.GREEN + Colors.BOLD)
    elif missing <= 2:
        estado = colored(f"⚠️   Estado general: proyecto incompleto ({missing} archivo(s) faltante(s))", Colors.YELLOW + Colors.BOLD)
    else:
        estado = colored(f"❌  Estado general: proyecto requiere atención ({missing} archivos faltantes)", Colors.RED + Colors.BOLD)

    print(f"  {estado}")

    if missing > 0:
        print()
        print(colored("  Archivos faltantes:", Colors.YELLOW))
        for r in results:
            if not r["found"]:
                print(f"    ✘ {r['path']}")
                print(f"      → {r['desc']}")

def print_footer():
    print()
    print_separator("═")
    print(colored("   SpotiDev DevOps | Fin del reporte", Colors.CYAN))
    print_separator("═")
    print()

# ─── Main ─────────────────────────────────────────────────

def main():
    # Cambiar al directorio del script para que las rutas relativas funcionen
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    print_header()

    results = [check_file(entry) for entry in FILES_TO_CHECK]
    found_count = print_results(results)

    print_summary(results, found_count)
    print_footer()

    # Código de salida: 0 si todo OK, 1 si hay faltantes
    sys.exit(0 if found_count == len(results) else 1)

if __name__ == "__main__":
    main()
"""
helper.py - Servicio auxiliar de estado del proyecto SpotiDev
Contenedor 2: Monitoreo y diagnóstico del entorno
"""

from flask import Flask, jsonify
import os
import sys
import platform
import datetime

app = Flask(__name__)

SERVICE_NAME    = "spotidev-helper"
SERVICE_VERSION = "1.0.0"

# Archivos del proyecto a verificar (rutas relativas al workspace)
PROJECT_FILES = [
    "README.md",
    "docker-compose.yml",
    "setup_project.sh",
    "project_report.py",
    "infraestructura-base.yaml",
    "app/Dockerfile",
    "helper/Dockerfile",
    ".github/workflows/ci.yml",
]

def check_project_files():
    """Verifica existencia de archivos clave del proyecto."""
    results = {}
    for f in PROJECT_FILES:
        results[f] = os.path.isfile(f"/{f}") or os.path.isfile(f)
    return results


@app.route("/status")
def status():
    file_checks = check_project_files()
    all_ok      = all(file_checks.values())

    return jsonify({
        "service":   SERVICE_NAME,
        "version":   SERVICE_VERSION,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "status":    "healthy" if all_ok else "degraded",
        "system": {
            "platform":    platform.system(),
            "python":      sys.version.split()[0],
            "hostname":    platform.node(),
            "architecture": platform.machine(),
        },
        "project_files": {
            k: "encontrado" if v else "no encontrado"
            for k, v in file_checks.items()
        },
        "project_ready": all_ok,
        "summary": "proyecto listo para validación" if all_ok else "proyecto incompleto – revisar archivos faltantes",
    })


@app.route("/health")
def health():
    return jsonify({
        "status":  "healthy",
        "service": SERVICE_NAME,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    })


@app.route("/")
def home():
    return jsonify({
        "service":     SERVICE_NAME,
        "description": "Servicio auxiliar de monitoreo y diagnóstico para SpotiDev",
        "endpoints": {
            "status": "GET /status → Estado completo del proyecto y sistema",
            "health": "GET /health → Health check simple del servicio",
        }
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=False)
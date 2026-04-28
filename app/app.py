"""
app.py - Aplicación Flask principal de SpotiDev
Contenedor 1: Servicio de bienvenida y reproducción
"""

from flask import Flask, jsonify
import os
import datetime

app = Flask(__name__)

APP_NAME    = "SpotiDev"
APP_VERSION = "1.0.0"
APP_ENV     = os.environ.get("APP_ENV", "development")


@app.route("/")
def home():
    return jsonify({
        "app":     APP_NAME,
        "version": APP_VERSION,
        "env":     APP_ENV,
        "message": "🎵 Bienvenido a SpotiDev – Tu plataforma de contenido digital",
        "status":  "running",
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "endpoints": {
            "home":   "GET /",
            "health": "GET /health",
            "info":   "GET /info",
        }
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "service": "spotidev-app",
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    })


@app.route("/info")
def info():
    return jsonify({
        "app":         APP_NAME,
        "version":     APP_VERSION,
        "environment": APP_ENV,
        "description": "Plataforma web para reproducir contenido digital y administrar perfiles de usuario",
        "features": [
            "Reproducción de audio y video",
            "Administración de perfiles",
            "Listas de reproducción personalizadas",
        ]
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=(APP_ENV == "development"))
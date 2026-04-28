#!/bin/bash

# ============================================================
# setup_project.sh
# Script de preparación del entorno Linux para SpotiDev
# Simula la instalación y configuración del entorno DevOps
# ============================================================

set -e  # Detener el script si ocurre un error

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # Sin color

# Función para imprimir encabezado
print_header() {
    echo ""
    echo -e "${CYAN}============================================================${NC}"
    echo -e "${CYAN}   🎵 SpotiDev - Preparación de Entorno DevOps${NC}"
    echo -e "${CYAN}============================================================${NC}"
    echo ""
}

# Función para imprimir paso
print_step() {
    echo -e "${BLUE}[PASO $1]${NC} $2"
}

# Función para imprimir éxito
print_ok() {
    echo -e "  ${GREEN}✔ $1${NC}"
}

# Función para imprimir advertencia
print_warn() {
    echo -e "  ${YELLOW}⚠ $1${NC}"
}

# Función para simular progreso
simulate_progress() {
    local message=$1
    echo -ne "  ⏳ $message"
    sleep 0.5
    echo -e "\r  ${GREEN}✔ $message${NC}"
}

# ─── INICIO ───────────────────────────────────────────────

print_header

echo -e "${YELLOW}Iniciando configuración del entorno...${NC}"
echo -e "Fecha: $(date '+%Y-%m-%d %H:%M:%S')"
echo -e "Usuario: $(whoami)"
echo -e "Sistema: $(uname -s) $(uname -r)"
echo ""

# ─── PASO 1: Actualizar paquetes ──────────────────────────
print_step "1" "Actualizando lista de paquetes del sistema..."
simulate_progress "Ejecutando: apt-get update"
simulate_progress "Ejecutando: apt-get upgrade -y"
print_ok "Paquetes del sistema actualizados correctamente."
echo ""

# ─── PASO 2: Instalar Git ─────────────────────────────────
print_step "2" "Instalando Git..."

if command -v git &>/dev/null; then
    GIT_VERSION=$(git --version)
    print_warn "Git ya está instalado: $GIT_VERSION"
else
    simulate_progress "Ejecutando: apt-get install -y git"
    print_ok "Git instalado correctamente."
fi

simulate_progress "Verificando instalación de Git"
print_ok "Git disponible en el sistema."
echo ""

# ─── PASO 3: Instalar Python3 ─────────────────────────────
print_step "3" "Instalando Python3 y pip..."

if command -v python3 &>/dev/null; then
    PYTHON_VERSION=$(python3 --version)
    print_warn "Python3 ya está instalado: $PYTHON_VERSION"
else
    simulate_progress "Ejecutando: apt-get install -y python3 python3-pip"
    print_ok "Python3 instalado correctamente."
fi

simulate_progress "Actualizando pip"
simulate_progress "Instalando dependencias: flask"
print_ok "Python3 y dependencias disponibles."
echo ""

# ─── PASO 4: Instalar Docker ──────────────────────────────
print_step "4" "Instalando Docker y Docker Compose..."

if command -v docker &>/dev/null; then
    DOCKER_VERSION=$(docker --version)
    print_warn "Docker ya está instalado: $DOCKER_VERSION"
else
    simulate_progress "Instalando dependencias de Docker"
    simulate_progress "Agregando repositorio oficial de Docker"
    simulate_progress "Ejecutando: apt-get install -y docker-ce docker-ce-cli"
    simulate_progress "Habilitando servicio Docker: systemctl enable docker"
    print_ok "Docker instalado correctamente."
fi

if command -v docker &>/dev/null && docker compose version &>/dev/null 2>&1; then
    print_warn "Docker Compose (plugin) ya está disponible."
elif command -v docker-compose &>/dev/null; then
    print_warn "Docker Compose ya está instalado."
else
    simulate_progress "Instalando Docker Compose plugin"
    print_ok "Docker Compose instalado correctamente."
fi

print_ok "Docker y Docker Compose listos."
echo ""

# ─── PASO 5: Crear estructura de carpetas ─────────────────
print_step "5" "Creando estructura de carpetas del proyecto..."

DIRS=(
    "app"
    "helper"
    ".github/workflows"
    "logs"
    "scripts"
)

for dir in "${DIRS[@]}"; do
    if [ -d "$dir" ]; then
        print_warn "Carpeta '$dir' ya existe, omitiendo."
    else
        mkdir -p "$dir"
        print_ok "Carpeta '$dir' creada."
    fi
done

echo ""

# ─── PASO 6: Verificación final ───────────────────────────
print_step "6" "Verificación final del entorno..."
echo ""

echo -e "  ${CYAN}Herramientas detectadas:${NC}"
command -v git &>/dev/null     && echo -e "  ${GREEN}✔${NC} git        → $(git --version)" || echo -e "  ${RED}✘${NC} git        → No encontrado"
command -v python3 &>/dev/null && echo -e "  ${GREEN}✔${NC} python3    → $(python3 --version)" || echo -e "  ${RED}✘${NC} python3    → No encontrado"
command -v docker &>/dev/null  && echo -e "  ${GREEN}✔${NC} docker     → $(docker --version)" || echo -e "  ${RED}✘${NC} docker     → No encontrado"
command -v pip3 &>/dev/null    && echo -e "  ${GREEN}✔${NC} pip3       → $(pip3 --version 2>/dev/null | awk '{print $1, $2}')" || echo -e "  ${YELLOW}⚠${NC} pip3       → No encontrado (opcional)"

echo ""
echo -e "  ${CYAN}Estructura de carpetas:${NC}"
for dir in "${DIRS[@]}"; do
    [ -d "$dir" ] && echo -e "  ${GREEN}✔${NC} $dir/" || echo -e "  ${RED}✘${NC} $dir/"
done

echo ""
echo -e "${CYAN}============================================================${NC}"
echo -e "${GREEN}   ✅ Entorno preparado correctamente para SpotiDev${NC}"
echo -e "${CYAN}============================================================${NC}"
echo ""
echo -e "Próximos pasos:"
echo -e "  1. Ejecuta ${YELLOW}docker-compose up --build${NC} para levantar los servicios"
echo -e "  2. Ejecuta ${YELLOW}python3 project_report.py${NC} para verificar el estado del proyecto"
echo ""
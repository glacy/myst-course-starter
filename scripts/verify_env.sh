#!/usr/bin/env bash

# ------------------------------------------------------------
# Verificación del entorno técnico oficial del curso
# Curso: Diseño semántico de documentos académicos
# ------------------------------------------------------------

set -e

# ANSI Colors
CYAN='\033[0;36m'
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "=============================================="
echo -e " ${CYAN}Verificación del entorno: frontmatter-academico${NC}"
echo -e "=============================================="
echo

# 1. Verificar entorno Conda activo
if [[ -z "$CONDA_DEFAULT_ENV" ]]; then
  echo -e "${RED}❌ ERROR: No hay ningún entorno Conda activo.${NC}"
  echo "   Active el entorno con:"
  echo "   conda activate frontmatter-academico"
  exit 1
fi

if [[ "$CONDA_DEFAULT_ENV" != "frontmatter-academico" ]]; then
  echo -e "${YELLOW}⚠ ADVERTENCIA: El entorno activo es '$CONDA_DEFAULT_ENV'${NC}"
  echo "   Se recomienda: 'frontmatter-academico'. Continuando..."
else
  echo -e "${GREEN}✔ Entorno Conda activo: $CONDA_DEFAULT_ENV${NC}"
fi
echo

# 2. Función auxiliar para verificar comandos
check_command () {
  local cmd=$1
  local name=$2

  if command -v "$cmd" &> /dev/null; then
    echo -e "${GREEN}✔ $name encontrado: $($cmd --version | head -n 1)${NC}"
  else
    echo -e "${RED}❌ ERROR: '$name' no está disponible en el entorno.${NC}"
    exit 1
  fi
}

# 3. Verificación de herramientas clave
check_command myst "MyST"
check_command pandoc "Pandoc"
check_command quarto "Quarto"
check_command jupyter-book "Jupyter Book"
check_command python3 "Python 3"

# 4. Verificación de librerías Python
if python3 -c "import yaml" &> /dev/null; then
  echo -e "${GREEN}✔ PyYAML encontrado${NC}"
else
  echo -e "${RED}❌ ERROR: 'PyYAML' no está disponible en el entorno (requerido para validar frontmatter).${NC}"
  exit 1
fi

echo
echo -e "=============================================="
echo -e " ${GREEN}✔ El entorno está correctamente configurado${NC}"
echo -e "=============================================="
echo
echo "Puede continuar con las actividades del curso."

#!/usr/bin/env bash

# ------------------------------------------------------------
# Official Course Environment Verification
# Myst Course Starter
# ------------------------------------------------------------

set -e

# ANSI Colors
CYAN='\033[0;36m'
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "=============================================="
echo -e " ${CYAN}Environment Verification: myst-course-starter${NC}"
echo -e "=============================================="
echo

# 1. Verify active Conda environment
if [[ -z "$CONDA_DEFAULT_ENV" ]]; then
  echo -e "${RED}❌ ERROR: No active Conda environment found.${NC}"
  echo "   Activate the environment with:"
  echo "   conda activate myst-course-starter"
  exit 1
fi

if [[ "$CONDA_DEFAULT_ENV" != "myst-course-starter" ]]; then
  echo -e "${YELLOW}⚠ WARNING: Active environment is '$CONDA_DEFAULT_ENV'${NC}"
  echo "   Recommended: 'myst-course-starter'. Continuing..."
else
  echo -e "${GREEN}✔ Active Conda environment: $CONDA_DEFAULT_ENV${NC}"
fi
echo

# 2. Helper function to verify commands
check_command () {
  local cmd=$1
  local name=$2

  if command -v "$cmd" &> /dev/null; then
    echo -e "${GREEN}✔ $name found: $($cmd --version | head -n 1)${NC}"
  else
    echo -e "${RED}❌ ERROR: '$name' is not available in the environment.${NC}"
    exit 1
  fi
}

# 3. Verification of key tools
check_command myst "MyST"
check_command pandoc "Pandoc"
# check_command quarto "Quarto"         # Removed (optional)
# check_command jupyter-book "Jupyter Book" # Removed (optional)
check_command python3 "Python 3"

# 4. Verification of Python libraries
if python3 -c "import yaml" &> /dev/null; then
  echo -e "${GREEN}✔ PyYAML found${NC}"
else
  echo -e "${RED}❌ ERROR: 'PyYAML' not available in environment (required for frontmatter validation).${NC}"
  exit 1
fi

echo
echo -e "=============================================="
echo -e " ${GREEN}✔ Environment is correctly configured${NC}"
echo -e "=============================================="
echo
echo "You can proceed with the course activities."

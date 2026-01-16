# Verificación del entorno técnico oficial del curso (Windows/PowerShell)
# Curso: Diseño semántico de documentos académicos

$ErrorActionPreference = "Stop"

# ANSI Colors
$CYAN = "$([char]27)[96m"
$GREEN = "$([char]27)[92m"
$RED = "$([char]27)[91m"
$YELLOW = "$([char]27)[33m"
$RESET = "$([char]27)[0m"

Write-Host "${CYAN}==============================================${RESET}"
Write-Host "${CYAN} Verificación del entorno: frontmatter-academico${RESET}"
Write-Host "${CYAN}==============================================${RESET}"
Write-Host ""

# 1. Verificar entorno Conda activo
# En PowerShell, las variables de entorno se acceden con $env:
if ([string]::IsNullOrEmpty($env:CONDA_DEFAULT_ENV)) {
    Write-Host "${RED}❌ ERROR: No hay ningún entorno Conda activo.${RESET}"
    Write-Host "   Active el entorno con:"
    Write-Host "   conda activate frontmatter-academico"
    exit 1
}

if ($env:CONDA_DEFAULT_ENV -ne "frontmatter-academico") {
    Write-Host "${YELLOW}⚠ ADVERTENCIA: El entorno activo es '$env:CONDA_DEFAULT_ENV'${RESET}"
    Write-Host "   Se recomienda: 'frontmatter-academico'. Continuando..."
} else {
    Write-Host "${GREEN}✔ Entorno Conda activo: $env:CONDA_DEFAULT_ENV${RESET}"
}
Write-Host ""

# 2. Función auxiliar para verificar comandos
function Check-Command {
    param (
        [string]$Command,
        [string]$Name
    )

    if (Get-Command $Command -ErrorAction SilentlyContinue) {
        # Intentar obtener versión. Algunos comandos imprimen a stderr o requieren argumentos específicos.
        # Aquí simplificamos mostrando solo que se encontró.
        Write-Host "${GREEN}✔ $Name encontrado${RESET}"
    } else {
        Write-Host "${RED}❌ ERROR: '$Name' no está disponible en el entorno.${RESET}"
        exit 1
    }
}

# 3. Verificación de herramientas clave
Check-Command "myst" "MyST"
Check-Command "pandoc" "Pandoc"
Check-Command "quarto" "Quarto"
Check-Command "jupyter-book" "Jupyter Book"
Check-Command "python" "Python 3"

# 4. Verificación de librerías Python
try {
    python -c "import yaml" | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "${GREEN}✔ PyYAML encontrado${RESET}"
    } else {
        throw "PyYAML check failed"
    }
} catch {
    Write-Host "${RED}❌ ERROR: 'PyYAML' no está disponible en el entorno (requerido para validar frontmatter).${RESET}"
    exit 1
}

Write-Host ""
Write-Host "${CYAN}==============================================${RESET}"
Write-Host "${GREEN}✔ El entorno está correctamente configurado${RESET}"
Write-Host "${CYAN}==============================================${RESET}"
Write-Host ""
Write-Host "Puede continuar con las actividades del curso."

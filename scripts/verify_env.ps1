# Official Course Environment Verification (Windows/PowerShell)
# Myst Course Starter

$ErrorActionPreference = "Stop"

# ANSI Colors
$CYAN = "$([char]27)[96m"
$GREEN = "$([char]27)[92m"
$RED = "$([char]27)[91m"
$YELLOW = "$([char]27)[33m"
$RESET = "$([char]27)[0m"

Write-Host "${CYAN}==============================================${RESET}"
Write-Host "${CYAN} Environment Verification: myst-course-starter${RESET}"
Write-Host "${CYAN}==============================================${RESET}"
Write-Host ""

# 1. Verify active Conda environment
# In PowerShell, env vars are accessed with $env:
if ([string]::IsNullOrEmpty($env:CONDA_DEFAULT_ENV)) {
    Write-Host "${RED}❌ ERROR: No active Conda environment found.${RESET}"
    Write-Host "   Activate the environment with:"
    Write-Host "   conda activate myst-course-starter"
    exit 1
}

if ($env:CONDA_DEFAULT_ENV -ne "myst-course-starter") {
    Write-Host "${YELLOW}⚠ WARNING: Active environment is '$env:CONDA_DEFAULT_ENV'${RESET}"
    Write-Host "   Recommended: 'myst-course-starter'. Continuing..."
} else {
    Write-Host "${GREEN}✔ Active Conda environment: $env:CONDA_DEFAULT_ENV${RESET}"
}
Write-Host ""

# 2. Helper function to verify commands
function Check-Command {
    param (
        [string]$Command,
        [string]$Name
    )

    if (Get-Command $Command -ErrorAction SilentlyContinue) {
        # Try to get version. Some commands print to stderr or require specific args.
        # Simplified to just show found.
        Write-Host "${GREEN}✔ $Name found${RESET}"
    } else {
        Write-Host "${RED}❌ ERROR: '$Name' is not available in the environment.${RESET}"
        exit 1
    }
}

# 3. Verification of key tools
Check-Command "myst" "MyST"
Check-Command "pandoc" "Pandoc"
# Check-Command "quarto" "Quarto" # Removed (optional)
# Check-Command "jupyter-book" "Jupyter Book" # Removed (optional)
Check-Command "python" "Python 3"

# 4. Verification of Python libraries
try {
    python -c "import yaml" | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "${GREEN}✔ PyYAML found${RESET}"
    } else {
        throw "PyYAML check failed"
    }
} catch {
    Write-Host "${RED}❌ ERROR: 'PyYAML' not available in environment (required for frontmatter validation).${RESET}"
    exit 1
}

Write-Host ""
Write-Host "${CYAN}==============================================${RESET}"
Write-Host "${GREEN}✔ Environment is correctly configured${RESET}"
Write-Host "${CYAN}==============================================${RESET}"
Write-Host ""
Write-Host "You can proceed with the course activities."

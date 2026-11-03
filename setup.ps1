param([string]$Workspace,[string]$Conda)
& (Join-Path $PSScriptRoot "scripts/launch.ps1") -Mode setup -Workspace $Workspace -Conda $Conda
exit $LASTEXITCODE

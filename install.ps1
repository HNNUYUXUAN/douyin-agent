param([string]$Workspace,[string]$SkillDir,[string]$Conda)
& (Join-Path $PSScriptRoot "scripts/launch.ps1") -Mode install -Workspace $Workspace -Conda $Conda -SkillDir $SkillDir
exit $LASTEXITCODE

param([string]$Workspace,[string]$Conda,[string]$SkillDir)
& (Join-Path $PSScriptRoot "scripts/launch.ps1") -Mode install -Workspace $Workspace -Conda $Conda -SkillDir $SkillDir
exit $LASTEXITCODE

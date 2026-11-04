param([string]$Workspace,[string]$SkillDir,[string]$Conda,[ValidateSet("codex","workbuddy")][string]$TargetHost="codex")
& (Join-Path $PSScriptRoot "scripts/launch.ps1") -Mode install -Workspace $Workspace -Conda $Conda -SkillDir $SkillDir -TargetHost $TargetHost
exit $LASTEXITCODE

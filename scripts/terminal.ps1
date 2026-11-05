# Read-only terminal discovery. A WSL bash executable is not a Git Bash candidate.
$ErrorActionPreference='Stop'
. (Join-Path $PSScriptRoot 'discovery.ps1')
Get-DATerminal | ConvertTo-Json

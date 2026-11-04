# Read-only terminal discovery. A WSL bash executable is not a Git Bash candidate.
$ErrorActionPreference='Stop'
$gitRoots=@($env:ProgramFiles,${env:ProgramFiles(x86)},$env:LOCALAPPDATA)
foreach($base in $gitRoots){
 if(-not $base){continue}
 foreach($rel in @('Git\bin\bash.exe','Programs\Git\bin\bash.exe')){
  $candidate=Join-Path $base $rel
  if(Test-Path -LiteralPath $candidate -PathType Leaf){
   $version=& $candidate --version
   if($LASTEXITCODE -eq 0){@{shell='git-bash';executable=$candidate;version=@($version)[0]}|ConvertTo-Json;exit 0}
  }
 }
}
$pwsh=Get-Command pwsh -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1
if($pwsh){@{shell='powershell7';executable=$pwsh.Source;version=(& $pwsh.Source -NoProfile -Command '$PSVersionTable.PSVersion.ToString()')}|ConvertTo-Json;exit 0}
$ps5=Join-Path $env:SystemRoot 'System32\WindowsPowerShell\v1.0\powershell.exe'
if(Test-Path -LiteralPath $ps5){@{shell='powershell51';executable=$ps5;version=(& $ps5 -NoProfile -Command '$PSVersionTable.PSVersion.ToString()')}|ConvertTo-Json;exit 0}
throw 'No supported Windows terminal found'

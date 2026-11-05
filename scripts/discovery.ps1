# Shared, read-only Windows discovery. Never enumerates environment values or profiles.
if($PSVersionTable.PSVersion.Major -eq 5){
 # A PS7 parent can leave its modules first in PSModulePath. Load this engine's signed system modules.
 foreach($module in @('Microsoft.PowerShell.Utility','Microsoft.PowerShell.Security')){
  Import-Module (Join-Path $PSHOME "Modules\$module\$module.psd1") -Force -ErrorAction Stop
 }
}
function Get-DATerminal {
 $paths=@()
 foreach($base in @($env:ProgramFiles,${env:ProgramFiles(x86)},$env:LOCALAPPDATA)){
  if($base){foreach($rel in @('Git\bin\bash.exe','Programs\Git\bin\bash.exe')){$paths+=Join-Path $base $rel}}
 }
 $portable=Join-Path $env:USERPROFILE '.workbuddy\binaries\PortableGit\versions'
 if(Test-Path -LiteralPath $portable){
  $paths+=@(Get-ChildItem -LiteralPath $portable -Directory | Sort-Object Name -Descending | ForEach-Object {Join-Path $_.FullName 'bin\bash.exe'})
 }
 foreach($candidate in $paths){
  if(Test-Path -LiteralPath $candidate -PathType Leaf){
   $v=& $candidate --version
   if($LASTEXITCODE -eq 0){return [pscustomobject]@{shell='git-bash';executable=$candidate;version=@($v)[0]}}
  }
 }
 $ps7=Get-Command pwsh -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1
 if($ps7){return [pscustomobject]@{shell='powershell7';executable=$ps7.Source;version=(& $ps7.Source -NoProfile -Command '$PSVersionTable.PSVersion.ToString()')}}
 $ps5=Join-Path $env:SystemRoot 'System32\WindowsPowerShell\v1.0\powershell.exe'
 if(Test-Path -LiteralPath $ps5){return [pscustomobject]@{shell='powershell51';executable=$ps5;version=(& $ps5 -NoProfile -Command '$PSVersionTable.PSVersion.ToString()')}}
 throw 'No supported Windows terminal found'
}

function Get-DAConda([string]$Explicit,[string]$Workspace) {
 $paths=@()
 if($Explicit){$paths=@($Explicit)}else{
  if($env:CONDA_EXE){$paths+=$env:CONDA_EXE}
  $cmd=Get-Command conda -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1
  if($cmd){$paths+=$cmd.Source}
  if($Workspace){$paths+=Join-Path $Workspace 'tools\miniconda3\Scripts\conda.exe'}
  foreach($root in @($env:USERPROFILE,$env:ProgramData,'D:\','C:\')){
   if($root){foreach($name in @('miniconda3','anaconda3','miniforge3','mc3')){$paths+=Join-Path $root "$name\Scripts\conda.exe"}}
  }
 }
 foreach($candidate in $paths){
  if(Test-Path -LiteralPath $candidate -PathType Leaf){
   $candidate=$ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($candidate)
   if([IO.Path]::GetExtension($candidate) -eq '.bat'){
    $exe=Join-Path (Split-Path (Split-Path $candidate -Parent) -Parent) 'Scripts\conda.exe'
    if(Test-Path -LiteralPath $exe){$candidate=$exe}
   }
   return $candidate
  }
 }
 return $null
}

function Assert-DAPlain([string]$Path) {
 $p=[IO.Path]::GetFullPath($Path)
 $current=$p
 while($current){
  if(Test-Path -LiteralPath $current){
   if((Get-Item -LiteralPath $current -Force).Attributes -band [IO.FileAttributes]::ReparsePoint){throw 'Linked paths are unsupported'}
  }
  $parent=[IO.Path]::GetDirectoryName($current)
  if($parent -eq $current){break};$current=$parent
 }
 return $p
}

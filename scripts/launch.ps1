param([ValidateSet('install','setup')][string]$Mode,[string]$Workspace,[string]$SkillDir,[string]$Conda)
$ErrorActionPreference='Stop'
if($PSVersionTable.PSVersion.Major -lt 5){throw 'Windows PowerShell 5.1 or PowerShell 7 is required.'}
$candidates=@()
if($Conda){$candidates=@($Conda)}else{
 if($env:CONDA_EXE){$candidates+=$env:CONDA_EXE}
 $cmd=Get-Command conda -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1
 if($cmd){$candidates+=$cmd.Source}
 foreach($root in @($env:USERPROFILE,$env:ProgramData)){
  if($root){foreach($name in @('miniconda3','anaconda3','miniforge3')){$candidates+=Join-Path $root "$name\Scripts\conda.exe"}}
 }
}
$found=$null
foreach($candidate in $candidates){
 if(Test-Path -LiteralPath $candidate -PathType Leaf){
  $candidate=$ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($candidate)
  if([IO.Path]::GetExtension($candidate) -eq '.bat'){
   $exe=Join-Path (Split-Path (Split-Path $candidate -Parent) -Parent) 'Scripts\conda.exe'
   if(Test-Path -LiteralPath $exe){$candidate=$exe}
  }
  $found=$candidate; break
 }
}
if(-not $found){throw 'Conda not found. Install from https://www.anaconda.com/docs/getting-started/miniconda/install or pass -Conda CONDA_EXE.'}
$base=& $found info --base
if($LASTEXITCODE -ne 0){throw 'Conda discovery failed; inspect the selected Conda installation.'}
$py=Join-Path ((@($base)[-1]).Trim()) 'python.exe'
if(-not(Test-Path -LiteralPath $py -PathType Leaf)){throw 'Conda base Python is missing.'}
$arguments=@('-B',(Join-Path $PSScriptRoot 'installer.py'),$Mode,'--conda',$found)
if($Workspace){$arguments+=@('--workspace',$ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($Workspace))}
if($SkillDir){$arguments+=@('--skill-dir',$ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($SkillDir))}
$prior=$env:PYTHONUTF8
try {$env:PYTHONUTF8='1'; & $py @arguments; $code=$LASTEXITCODE}finally{$env:PYTHONUTF8=$prior}
exit $code

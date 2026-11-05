param([ValidateSet('install','setup')][string]$Mode,[string]$Workspace,[string]$SkillDir,[string]$Conda,[ValidateSet("codex","workbuddy")][string]$TargetHost="codex")
$ErrorActionPreference='Stop'
if($PSVersionTable.PSVersion.Major -lt 5){throw 'Windows PowerShell 5.1 or PowerShell 7 is required.'}
. (Join-Path $PSScriptRoot 'discovery.ps1')
$found=Get-DAConda $Conda $Workspace
if(-not $found){throw 'Conda not found. Install from https://www.anaconda.com/docs/getting-started/miniconda/install or pass -Conda CONDA_EXE.'}
$savedPreference=$ErrorActionPreference
try {$ErrorActionPreference='Continue'; $base=& $found info --base; $discoveryCode=$LASTEXITCODE}finally{$ErrorActionPreference=$savedPreference}
if($discoveryCode -ne 0){throw 'Conda discovery failed; inspect the selected Conda installation.'}
$py=Join-Path ((@($base)[-1]).Trim()) 'python.exe'
if(-not(Test-Path -LiteralPath $py -PathType Leaf)){throw 'Conda base Python is missing.'}
$arguments=@('-B',(Join-Path $PSScriptRoot 'installer.py'),$Mode,'--conda',$found,'--host',$TargetHost)
if($Workspace){$arguments+=@('--workspace',$ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($Workspace))}
if($SkillDir){$arguments+=@('--skill-dir',$ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($SkillDir))}
$prior=$env:PYTHONUTF8
try {$env:PYTHONUTF8='1'; $ErrorActionPreference='Continue'; & $py @arguments; $code=$LASTEXITCODE}finally{$env:PYTHONUTF8=$prior; $ErrorActionPreference=$savedPreference}
exit $code

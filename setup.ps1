param([string]$Workspace, [string]$Conda)
$ErrorActionPreference='Stop'
if (-not $Workspace) {
  $suggested=if(Test-Path 'D:\'){'D:\douyin-agent'}else{Join-Path $env:USERPROFILE 'douyin-agent'}
  $Workspace=Read-Host "Workspace [$suggested]"
  if(-not $Workspace){$Workspace=$suggested}
}
$Workspace=[IO.Path]::GetFullPath($Workspace)
if($Workspace.Length -gt 85){throw 'Choose a shorter workspace path (85 characters maximum)'}
if(-not $Conda){
  $candidates=@((Join-Path $env:ProgramData 'miniconda3\Scripts\conda.exe'),(Join-Path $env:USERPROFILE 'miniconda3\Scripts\conda.exe'),$env:CONDA_EXE)
  $cmd=Get-Command conda -ErrorAction SilentlyContinue
  if($cmd){$candidates+= $cmd.Source}
  $Conda=$candidates | Where-Object {$_ -and (Test-Path -LiteralPath $_)} | Select-Object -First 1
}
if(-not $Conda){throw 'Install Miniconda from https://www.anaconda.com/docs/getting-started/miniconda/install or pass -Conda with its executable path.'}
foreach($name in @('out','cache','envs','qa')){New-Item -ItemType Directory -Force -Path (Join-Path $Workspace $name)|Out-Null}
$python=Join-Path $Workspace 'envs\runtime\python.exe'
$oldUtf8=$env:PYTHONUTF8
try {
  $env:PYTHONUTF8='1'
  if(-not(Test-Path -LiteralPath $python)){
    & $Conda create -y --override-channels -c conda-forge --prefix (Join-Path $Workspace 'envs\runtime') --file (Join-Path $PSScriptRoot 'conda-win-64.lock')
    if($LASTEXITCODE -ne 0){throw 'Conda creation failed; existing files retained'}
  }
  & $python -c "import sys; assert sys.version_info[:2]==(3,12), 'Expected Python 3.12'"
  if($LASTEXITCODE -ne 0){throw 'Wrong Python environment'}
  & $python -m pip install -r (Join-Path $PSScriptRoot 'requirements.lock')
  if($LASTEXITCODE -ne 0){throw 'Dependency installation failed'}
  if(-not(Test-Path -LiteralPath (Join-Path $Workspace '.env'))){Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'env.template') -Destination (Join-Path $Workspace '.env')}
  @{schema_version=1;workspace=$Workspace;python=$python;skill_root=$PSScriptRoot}|ConvertTo-Json|Set-Content -LiteralPath (Join-Path $Workspace 'workspace.json') -Encoding utf8
  & $python (Join-Path $PSScriptRoot 'scripts\da.py') --workspace $Workspace doctor
} finally {$env:PYTHONUTF8=$oldUtf8}

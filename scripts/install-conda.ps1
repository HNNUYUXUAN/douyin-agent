param([string]$Workspace,[string]$Installer,[string]$Sha256,[ValidateRange(1,900)][int]$TimeoutSeconds=900)
$ErrorActionPreference='Stop'
. (Join-Path $PSScriptRoot 'discovery.ps1')

function Test-DACondaReady([string]$Destination){
 $exe=Join-Path $Destination 'Scripts\conda.exe';$py=Join-Path $Destination 'python.exe'
 if(-not(Test-Path -LiteralPath $exe -PathType Leaf) -or -not(Test-Path -LiteralPath $py -PathType Leaf)){return $false}
 $prior=$ErrorActionPreference
 try{
  $ErrorActionPreference='Continue'
  $null=& $exe --version; $a=$LASTEXITCODE
  $null=& $py -B -c 'import sys; sys.exit(0 if sys.version_info >= (3,10) else 1)';$b=$LASTEXITCODE
 }finally{$ErrorActionPreference=$prior}
 return ($a -eq 0 -and $b -eq 0)
}

function Invoke-DACondaInstall([string]$Workspace,[string]$Installer,[string]$Sha256,[int]$TimeoutSeconds){
 $arch=if($env:PROCESSOR_ARCHITEW6432){$env:PROCESSOR_ARCHITEW6432}else{$env:PROCESSOR_ARCHITECTURE}
 if($arch -ne 'AMD64'){throw 'This Conda workflow supports Windows x64 only'}
 if(-not $Workspace -or -not $Installer -or $Sha256 -notmatch '^[a-fA-F0-9]{64}$'){throw 'Provide Workspace, reviewed official Installer and its recorded SHA256'}
 $w=Assert-DAPlain $Workspace;$file=Assert-DAPlain $Installer
 $destination=Assert-DAPlain (Join-Path $w 'tools\miniconda3')
 if($destination -match '\s' -or $destination.Contains('"')){throw 'Conda silent destination must have no spaces or quotes'}
 if(Test-Path -LiteralPath $destination){
  if(Test-DACondaReady $destination){return [pscustomobject]@{status='reused';destination=$destination}}
  throw 'Existing incomplete directory preserved; inspect ownership and logs before any cleanup'
 }
 $hash=(Get-FileHash -LiteralPath $file -Algorithm SHA256).Hash
 if($hash -ne $Sha256){throw 'Installer SHA256 mismatch'}
 $signature=Get-AuthenticodeSignature -LiteralPath $file
 if($signature.Status -ne 'Valid' -or $signature.SignerCertificate.Subject -notmatch '(?i)\bAnaconda'){throw 'Expected valid Anaconda Authenticode signature'}
 if((Get-FileHash -LiteralPath $file -Algorithm SHA256).Hash -ne $hash){throw 'Installer changed during inspection'}
 $null=New-Item -ItemType Directory -Path (Split-Path $destination -Parent) -Force
 # Reserve the new destination without Force; a concurrent existing directory stops installation.
 $null=New-Item -ItemType Directory -Path $destination -ErrorAction Stop
 $proc=Start-Process -FilePath $file -ArgumentList @('/InstallationType=JustMe','/RegisterPython=0','/AddToPath=0','/S',"/D=$destination") -WindowStyle Hidden -PassThru
 $timer=[Diagnostics.Stopwatch]::StartNew();$nextProgress=0
 while($timer.Elapsed.TotalSeconds -lt $TimeoutSeconds){
  $proc.Refresh()
  if($proc.HasExited -and $proc.ExitCode -ne 0){throw "Conda installer failed; exit=$($proc.ExitCode); preserved=$destination"}
  if($proc.HasExited -and (Test-DACondaReady $destination)){
   return [pscustomobject]@{status='installed';destination=$destination;sha256=$hash;signature='Valid Anaconda';seconds=[math]::Round($timer.Elapsed.TotalSeconds,2)}
  }
  if($timer.Elapsed.TotalSeconds -ge $nextProgress){
   Write-Host (@{event='progress';stage='wait_conda';seconds=[int]$timer.Elapsed.TotalSeconds} | ConvertTo-Json -Compress)
   $nextProgress+=15
  }
  Start-Sleep -Milliseconds 1000
 }
 throw "Conda readiness timeout; preserve $destination and installer process $($proc.Id); inspect before retry. No process was terminated."
}
if($MyInvocation.InvocationName -ne '.'){
 Invoke-DACondaInstall $Workspace $Installer $Sha256 $TimeoutSeconds | ConvertTo-Json
}

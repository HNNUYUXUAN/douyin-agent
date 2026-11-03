param([string]$Workspace,[string]$SkillDir,[string]$Conda)
$ErrorActionPreference='Stop'
$src=[IO.Path]::GetFullPath($PSScriptRoot)
if(-not $Workspace){$suggested=if(Test-Path 'D:\'){'D:\douyin-agent'}else{Join-Path $env:USERPROFILE 'douyin-agent'}; $Workspace=Read-Host "Workspace [$suggested]"; if(-not $Workspace){$Workspace=$suggested}}
$Workspace=[IO.Path]::GetFullPath($Workspace)
if(-not $SkillDir){$base=if($env:CODEX_HOME){$env:CODEX_HOME}else{Join-Path $env:USERPROFILE '.codex'}; $SkillDir=Join-Path $base 'skills\douyin-agent'}
$SkillDir=[IO.Path]::GetFullPath($SkillDir)
if($SkillDir -eq $src){throw 'Source and installation must differ'}
function Assert-PlainPath([string]$Path) {
 $p=[IO.Path]::GetFullPath($Path)
 while($p){
  if((Test-Path -LiteralPath $p) -and ((Get-Item -LiteralPath $p -Force).Attributes -band [IO.FileAttributes]::ReparsePoint)){throw "Linked path unsupported: $p"}
  $parent=Split-Path $p -Parent; if($parent -eq $p){break}; $p=$parent
 }
}
function Safe-Relative([string]$Rel) {
 if(-not $Rel -or $Rel -notmatch '^[A-Za-z0-9_.\-/]+$' -or [IO.Path]::IsPathRooted($Rel) -or ($Rel -split '[/\\]') -contains '..'){throw 'Unsafe manifest path'}
}
Assert-PlainPath $SkillDir
Assert-PlainPath $Workspace
if($Workspace -eq $SkillDir -or $Workspace.StartsWith($SkillDir.TrimEnd('\')+'\',[StringComparison]::OrdinalIgnoreCase)){throw 'Workspace must be outside installed skill directory'}
$manifest=Get-Content -LiteralPath (Join-Path $src 'delivery.json') -Raw | ConvertFrom-Json
$files=@($manifest.files)+@('delivery.json')
if(@($files | Select-Object -Unique).Count -ne $files.Count){throw 'Duplicate manifest files'}
$old=$null; $receipt=Join-Path $SkillDir 'installed.json'
if(Test-Path -LiteralPath $SkillDir){
 if((Get-Item -LiteralPath $SkillDir).Attributes -band [IO.FileAttributes]::ReparsePoint){throw 'Linked installation unsupported'}
 if(Test-Path -LiteralPath $receipt){$old=Get-Content -LiteralPath $receipt -Raw | ConvertFrom-Json}
 elseif(@(Get-ChildItem -LiteralPath $SkillDir -Force).Count){throw 'Existing installation has no hash receipt; inspect before adoption'}
}
$hashes=@{}
foreach($rel in $files){
 Safe-Relative $rel
 $source=Join-Path $src $rel; $target=Join-Path $SkillDir $rel
 Assert-PlainPath $source
 Assert-PlainPath $target
 if($target.Length -gt 160){throw 'Installation path exceeds 160 characters'}
 if(-not(Test-Path -LiteralPath $source -PathType Leaf)){throw "Missing release file: $rel"}
 $hashes[$rel]=(Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash.ToLowerInvariant()
 if(Test-Path -LiteralPath $target){
  $expected=if($old -and $old.hashes){$old.hashes.PSObject.Properties[$rel].Value}else{$null}
  $actual=(Get-FileHash -LiteralPath $target -Algorithm SHA256).Hash.ToLowerInvariant()
  if(-not $expected -and $old -and $rel -eq 'delivery.json' -and $manifest.previous_manifests){
   $known=$manifest.previous_manifests.PSObject.Properties[$old.version].Value
   if($known -contains $actual){$expected=$actual}
  }
  if($actual -ne $hashes[$rel] -and (-not $expected -or $actual -ne $expected)){throw "Local modification conflict: $rel"}
 }
}
if($old){foreach($prop in $old.hashes.PSObject.Properties){
 $rel=$prop.Name
 Safe-Relative $rel
 $p=Join-Path $SkillDir $rel
 Assert-PlainPath $p
 if(-not(Test-Path -LiteralPath $p) -or (Get-FileHash -LiteralPath $p -Algorithm SHA256).Hash.ToLowerInvariant() -ne $prop.Value){throw "Old file changed: $rel"}
}}
# Environment setup is authorized by invoking installation; keys are never printed.
& (Join-Path $src 'setup.ps1') -Workspace $Workspace -Conda $Conda
if($LASTEXITCODE -and $LASTEXITCODE -ne 0){throw 'Setup failed'}
$backup=Join-Path $Workspace ('backups\install-'+[DateTime]::UtcNow.ToString('yyyyMMdd-HHmmss')+'-'+[Guid]::NewGuid().ToString('N').Substring(0,6))
if($old){
 New-Item -ItemType Directory -Force -Path $backup | Out-Null
 $backupFiles=@(@($old.hashes.PSObject.Properties.Name)+@($files | Where-Object {Test-Path -LiteralPath (Join-Path $SkillDir $_)})+@('installed.json') | Sort-Object -Unique)
 foreach($rel in $backupFiles){
  $to=Join-Path $backup $rel; New-Item -ItemType Directory -Force -Path (Split-Path $to) | Out-Null; Copy-Item -LiteralPath (Join-Path $SkillDir $rel) -Destination $to
 }
}
$written=@(); $existed=@{}
try {
 foreach($rel in $files){
  $to=Join-Path $SkillDir $rel; $existed[$rel]=Test-Path -LiteralPath $to
  New-Item -ItemType Directory -Force -Path (Split-Path $to) | Out-Null
  Copy-Item -LiteralPath (Join-Path $src $rel) -Destination $to; $written+=$rel
 }
 $receiptTemp=$receipt+'.tmp'
 @{schema_version=1;version=$manifest.version;hashes=$hashes;workspace=$Workspace;python=(Join-Path $Workspace 'envs\runtime\python.exe')} | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $receiptTemp -Encoding utf8
 Move-Item -LiteralPath $receiptTemp -Destination $receipt -Force
} catch {
 foreach($rel in $written){$to=Join-Path $SkillDir $rel; $prior=Join-Path $backup $rel; if(Test-Path -LiteralPath $prior){Copy-Item -LiteralPath $prior -Destination $to -Force}elseif(-not $existed[$rel]){Remove-Item -LiteralPath $to}}
 if($old -and (Test-Path -LiteralPath (Join-Path $backup 'installed.json'))){Copy-Item -LiteralPath (Join-Path $backup 'installed.json') -Destination $receipt -Force}
 elseif(-not $old -and (Test-Path -LiteralPath $receipt)){Remove-Item -LiteralPath $receipt}
 throw
}
$py=Join-Path $Workspace 'envs\runtime\python.exe'
& $py -B -c 'import sys; from pathlib import Path; sys.path.insert(0,sys.argv[1]); from onboarding import context; from legacy import write; write(Path(sys.argv[2])/"agent-context.json",context(Path(sys.argv[2]),sys.argv[3]))' (Join-Path $SkillDir 'scripts') $Workspace $manifest.version
if($LASTEXITCODE -ne 0){throw 'Installed; context write failed. Inspect before retry.'}
@{status='installed';version=$manifest.version;skill_dir=$SkillDir;workspace=$Workspace;backup=$(if($old){$backup}else{$null});next='Read AGENT_INSTALL.md and run onboard --check; verify host capabilities separately.'} | ConvertTo-Json

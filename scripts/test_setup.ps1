# Isolated fixtures only. No installer, browser, credential or registry mutation.
$ErrorActionPreference='Stop'
. (Join-Path $PSScriptRoot 'install-conda.ps1')
$fixture=[IO.Path]::GetFullPath((Join-Path $env:TEMP ('da-setup-'+[guid]::NewGuid().ToString('N'))))
$null=New-Item -ItemType Directory -Path $fixture
$script:count=0
function Assert($Condition,[string]$Message){if(-not $Condition){throw $Message};$script:count++}
function Reject([scriptblock]$Action){$bad=$false;try{& $Action | Out-Null}catch{$bad=$true};Assert $bad 'Expected rejection'}
try{
 $missing=Join-Path $fixture 'not-created'
 $snapshot=@(Get-ChildItem -LiteralPath $fixture -Recurse -Force).Count
 $result=(& (Join-Path $PSScriptRoot 'preflight.ps1') -Workspace $missing -TargetHost workbuddy | ConvertFrom-Json)
 Assert (-not(Test-Path -LiteralPath $missing)) 'Preflight must not create workspace'
 Assert (@(Get-ChildItem -LiteralPath $fixture -Recurse -Force).Count -eq $snapshot) 'Preflight is read-only'
 Assert ($result.required_docs.Count -eq 6) 'One-language setup pack'
 Assert ($result.terminal.shell -in @('git-bash','powershell7','powershell51')) 'Supported terminal'
 Assert (-not $result.cloud_verified) 'No cloud verification'
 Assert ($result.workspace_write -eq 'unverified') 'Read-only cannot infer write permission'
 $exported=Join-Path $fixture 'exported';$null=New-Item -ItemType Directory -Path $exported
 [IO.File]::WriteAllText((Join-Path $exported 'installed.json'),'{"schema_version":1,"version":"2.5.1","hashes":{}}')
 $exportCheck=(& (Join-Path $PSScriptRoot 'preflight.ps1') -Workspace $missing -SkillDir $exported -TargetHost workbuddy | ConvertFrom-Json)
 Assert (-not $exportCheck.installation_matches) 'Export receipt alone is not an installed workspace'
 Assert (-not(Test-Path -LiteralPath $missing)) 'Export receipt check remains read-only'
 $file=Join-Path $fixture 'official-fixture.exe';[IO.File]::WriteAllText($file,'mock executable, never executed')
 $digest=(Get-FileHash -LiteralPath $file -Algorithm SHA256).Hash
 $script:sigGood=$true;$script:ready=$true;$script:startCount=0;$script:exitCode=0
 function Get-AuthenticodeSignature {param($LiteralPath)
  [pscustomobject]@{Status=$(if($script:sigGood){'Valid'}else{'NotSigned'});SignerCertificate=[pscustomobject]@{Subject='CN=Anaconda, Inc.'}}
 }
 function Start-Process {param($FilePath,$ArgumentList,$WindowStyle,[switch]$PassThru)
  Assert ($WindowStyle -eq 'Hidden') 'Installer starts hidden'
  Assert ($ArgumentList[-1] -like '/D=*') 'NSIS destination is final argument'
  $script:startCount++
  $p=[pscustomobject]@{HasExited=$true;ExitCode=$script:exitCode;Id=9876}
  $p | Add-Member -MemberType ScriptMethod -Name Refresh -Value {}
  return $p
 }
 function Test-DACondaReady {param($Destination) return $script:ready}
 $ws=Join-Path $fixture 'success'
 $ok=Invoke-DACondaInstall $ws $file $digest 1
 Assert ($ok.status -eq 'installed') 'Wait for readiness after parent exit'
 Assert ($script:startCount -eq 1) 'One install process'
 $ok=Invoke-DACondaInstall $ws $file $digest 1
 Assert ($ok.status -eq 'reused') 'Reuse ready destination'
 Assert ($script:startCount -eq 1) 'No duplicate installer on reuse'
 Reject {Invoke-DACondaInstall (Join-Path $fixture 'bad-hash') $file ('0'*64) 1}
 $script:sigGood=$false
 Reject {Invoke-DACondaInstall (Join-Path $fixture 'bad-signature') $file $digest 1}
 $script:sigGood=$true;$script:ready=$false
 Reject {Invoke-DACondaInstall $ws $file $digest 1}
 Assert (Test-Path -LiteralPath (Join-Path $ws 'tools\miniconda3')) 'Incomplete target is preserved'
 $timeout=Join-Path $fixture 'timeout'
 Reject {Invoke-DACondaInstall $timeout $file $digest 1}
 Assert (Test-Path -LiteralPath (Join-Path $timeout 'tools\miniconda3')) 'Timeout preserves new destination'
 $script:exitCode=7
 Reject {Invoke-DACondaInstall (Join-Path $fixture 'exit-seven') $file $digest 1}
 Reject {Invoke-DACondaInstall (Join-Path $fixture 'has space') $file $digest 1}
 @{passed=$true;assertions=$script:count;scope='isolated mocked Conda lifetime/signature/hash fixtures and real read-only preflight';ps=$PSVersionTable.PSVersion.ToString()} | ConvertTo-Json
}finally{
 $resolved=[IO.Path]::GetFullPath($fixture)
 $tempRoot=[IO.Path]::GetFullPath($env:TEMP).TrimEnd('\')+'\'
 if(-not $resolved.StartsWith($tempRoot,[StringComparison]::OrdinalIgnoreCase) -or (Split-Path $resolved -Leaf) -notlike 'da-setup-*'){throw 'Fixture cleanup path outside TEMP'}
 Remove-Item -LiteralPath $resolved -Recurse -Force
}

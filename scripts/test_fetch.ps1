param([string]$SourceRoot=(Split-Path $PSScriptRoot -Parent))
$ErrorActionPreference='Stop'
$testRoot=Join-Path ([IO.Path]::GetTempPath()) ('daf-'+[Guid]::NewGuid().ToString('N').Substring(0,6))
New-Item -ItemType Directory -Path $testRoot | Out-Null
$target=Join-Path $testRoot 'repo'
$global:FetchFixtureRoot=$SourceRoot
$global:FetchFixtureBad=$false
function FileDigest([string]$Path){
 $digest=[Security.Cryptography.SHA256]::Create()
 try{return [BitConverter]::ToString($digest.ComputeHash([IO.File]::ReadAllBytes($Path)))}finally{$digest.Dispose()}
}
function global:Invoke-WebRequest {
 param([switch]$UseBasicParsing,[string]$Uri,[string]$OutFile)
 $prefix='https://raw.githubusercontent.com/HNNUYUXUAN/douyin-agent/v2.3.0/'
 if(-not $Uri.StartsWith($prefix)){throw 'Unexpected origin'}
 $rel=$Uri.Substring($prefix.Length)
 if($global:FetchFixtureBad){return @{Content='{"schema_version":1,"name":"douyin-agent","files":["../escape.md"]}'}}
 if($OutFile){Copy-Item -LiteralPath (Join-Path $global:FetchFixtureRoot $rel) -Destination $OutFile}
 else{return @{Content=[IO.File]::ReadAllText((Join-Path $global:FetchFixtureRoot $rel))}}
}
try {
 & (Join-Path $SourceRoot 'fetch.ps1') -Destination $target -Ref v2.3.0 | Out-Null
 $manifest=Get-Content -Raw -LiteralPath (Join-Path $SourceRoot 'delivery.json') | ConvertFrom-Json
 foreach($rel in (@($manifest.files)+@('delivery.json'))){
  if((FileDigest (Join-Path $target $rel)) -ne (FileDigest (Join-Path $SourceRoot $rel))){throw 'Fixture download mismatch'}
 }
 $failed=$false;try {& (Join-Path $SourceRoot 'fetch.ps1') -Destination $target | Out-Null}catch{$failed=$true}
 if(-not $failed){throw 'Existing directory was not protected'}
 $global:FetchFixtureBad=$true
 $failed=$false;try {& (Join-Path $SourceRoot 'fetch.ps1') -Destination (Join-Path $testRoot 'bad') | Out-Null}catch{$failed=$true}
 if(-not $failed -or (Test-Path -LiteralPath (Join-Path $testRoot 'escape.md'))){throw 'Manifest traversal protection failed'}
 Write-Output 'PASS: simulated no-Git source fetch, hashes, existing-directory and traversal protection'
} finally {
 Remove-Item Function:\Invoke-WebRequest -ErrorAction SilentlyContinue
 # Test fixtures are disposable; verify the resolved target before recursive cleanup.
 $resolved=[IO.Path]::GetFullPath($testRoot)
 $tempBase=[IO.Path]::GetFullPath([IO.Path]::GetTempPath())
 if($resolved.StartsWith($tempBase,[StringComparison]::OrdinalIgnoreCase) -and (Split-Path $resolved -Leaf) -like 'daf-*'){
  Remove-Item -LiteralPath $resolved -Recurse -Force
 }
}

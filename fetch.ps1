param([Parameter(Mandatory=$true)][string]$Destination,[string]$Ref='v2.3.0')
$ErrorActionPreference='Stop'
# Bootstrap needs Windows PowerShell only; it does not need Git, Python or Conda.
if($Ref -notmatch '^[A-Za-z0-9._-]+$'){throw 'Use a release tag or commit id.'}
$target=$ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($Destination)
if(Test-Path -LiteralPath $target){throw 'Choose a new destination; existing directories are preserved.'}
if($target.Length -gt 75){throw 'Choose a shorter source path (75 characters maximum).'}
$parent=Split-Path $target -Parent
while($parent){
 if((Test-Path -LiteralPath $parent) -and ((Get-Item -LiteralPath $parent).Attributes -band [IO.FileAttributes]::ReparsePoint)){throw 'Linked paths are unsupported.'}
 $next=Split-Path $parent -Parent;if($next -eq $parent){break};$parent=$next
}
[Net.ServicePointManager]::SecurityProtocol=[Net.ServicePointManager]::SecurityProtocol -bor [Net.SecurityProtocolType]::Tls12
$base="https://raw.githubusercontent.com/HNNUYUXUAN/douyin-agent/$Ref"
$response=Invoke-WebRequest -UseBasicParsing -Uri "$base/delivery.json"
$manifest=$response.Content | ConvertFrom-Json
if($manifest.name -ne 'douyin-agent' -or $manifest.schema_version -ne 1){throw 'Unexpected release manifest.'}
$paths=@($manifest.files)+@('delivery.json')
$seen=@{}
foreach($rel in $paths){
 if($rel -notmatch '^[A-Za-z0-9_.\-/]+$' -or $rel.StartsWith('/') -or ($rel.Split('/') | Where-Object {$_ -eq '' -or $_ -eq '.' -or $_ -eq '..'})){throw 'Unsafe manifest path.'}
 if($seen.ContainsKey($rel)){throw 'Duplicate release path.'};$seen[$rel]=$true
 if((Join-Path $target $rel).Length -gt 160){throw 'Release path too long.'}
}
New-Item -ItemType Directory -Path $target | Out-Null
foreach($rel in $paths){
 $path=Join-Path $target $rel
 New-Item -ItemType Directory -Path (Split-Path $path -Parent) -Force | Out-Null
 Invoke-WebRequest -UseBasicParsing -Uri "$base/$rel" -OutFile $path
}
@{status='downloaded_review_before_install';source=$base;version=$manifest.version;destination=$target;files=$paths.Count} | ConvertTo-Json

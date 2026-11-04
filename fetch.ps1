param([Parameter(Mandatory=$true)][string]$Destination,[string]$Ref='v2.4.0')
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
$archive=$null;$zip=$null;$archiveRoot=$null;$commit=$Ref
try {$response=Invoke-WebRequest -UseBasicParsing -Uri "$base/delivery.json"}catch{
 # Public API bootstrap: the script itself can be retrieved through the contents API.
 if($Ref -notmatch '^[a-fA-F0-9]{40}$'){
  $resolved=Invoke-WebRequest -UseBasicParsing -Uri "https://api.github.com/repos/HNNUYUXUAN/douyin-agent/commits/$Ref"
  $commit=($resolved.Content | ConvertFrom-Json).sha
 }
 if($commit -notmatch '^[a-fA-F0-9]{40}$'){throw 'Unable to resolve an immutable public commit'}
 $archive=Join-Path ([IO.Path]::GetTempPath()) ('da-fetch-'+[guid]::NewGuid().ToString('N')+'.zip')
 try {
  Invoke-WebRequest -UseBasicParsing -Uri "https://codeload.github.com/HNNUYUXUAN/douyin-agent/zip/$commit" -OutFile $archive
  if((Get-Item -LiteralPath $archive).Length -gt 104857600){throw 'Release archive exceeds limit'}
  Add-Type -AssemblyName System.IO.Compression.FileSystem
  $zip=[IO.Compression.ZipFile]::OpenRead($archive)
  $entries=@($zip.Entries | Where-Object {$_.FullName -match '^[^/]+/delivery.json$'})
  if($entries.Count -ne 1){throw 'Unexpected archive root'}
  $archiveRoot=$entries[0].FullName.Substring(0,$entries[0].FullName.Length-'delivery.json'.Length)
  foreach($entry in $zip.Entries){
   if(-not $entry.FullName.StartsWith($archiveRoot) -or $entry.FullName.Contains('\') -or ($entry.FullName.Split('/') -contains '..') -or (($entry.ExternalAttributes -shr 16) -band 61440) -eq 40960){throw 'Unsafe archive entry'}
  }
  $reader=New-Object IO.StreamReader($entries[0].Open())
  try{$response=@{Content=$reader.ReadToEnd()}}finally{$reader.Dispose()}
 }catch{if($zip){$zip.Dispose()};if($archive -and (Test-Path -LiteralPath $archive)){Remove-Item -LiteralPath $archive};throw}
}
try {
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
 if($zip){
  $entry=$zip.GetEntry($archiveRoot+$rel)
  if(-not $entry -or $entry.Length -gt 20971520){throw 'Missing or oversized allowlisted file'}
  $inputStream=$entry.Open();$outputStream=[IO.File]::Create($path)
  try{$inputStream.CopyTo($outputStream)}finally{$inputStream.Dispose();$outputStream.Dispose()}
 }else{Invoke-WebRequest -UseBasicParsing -Uri "$base/$rel" -OutFile $path}
}
@{status='downloaded_review_before_install';source=if($zip){'github-codeload'}else{$base};ref=$commit;version=$manifest.version;destination=$target;files=$paths.Count} | ConvertTo-Json
}finally{if($zip){$zip.Dispose()};if($archive -and (Test-Path -LiteralPath $archive)){Remove-Item -LiteralPath $archive}}

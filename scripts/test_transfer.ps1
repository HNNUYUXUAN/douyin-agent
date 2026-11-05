$ErrorActionPreference='Stop'
. (Join-Path $PSScriptRoot 'download-dependency.ps1')
$fixture=[IO.Path]::GetFullPath((Join-Path $env:TEMP ('da-range-'+[guid]::NewGuid().ToString('N'))));$null=New-Item -ItemType Directory -Path $fixture
$script:count=0
function Assert($Value,$Message){if(-not $Value){throw $Message};$script:count++}
function Reject([scriptblock]$Action){$failed=$false;try{& $Action|Out-Null}catch{$failed=$true};Assert $failed 'Expected rejection'}
$script:bytes=[Text.Encoding]::ASCII.GetBytes(('0123456789'*100));$script:bad='';$script:segmentCounts=@{}
$algorithm=[Security.Cryptography.SHA256]::Create();try{$digest=([BitConverter]::ToString($algorithm.ComputeHash($script:bytes))).Replace('-','')}finally{$algorithm.Dispose()}
function Start-DACurl([string]$Url,[string]$File,[string]$Header,[string]$Range,[string]$Validator){
 $code=0
 if(-not $Range){[IO.File]::WriteAllBytes($File,@(1,2,3));[IO.File]::WriteAllText($Header,"HTTP/1.1 200 OK`r`n`r`n");$code=28}
 else{
  $start,$end=$Range -split '-';$data=$script:bytes[[int]$start..[int]$end];$etag='"stable"'
  if($script:bad -eq 'etag' -and [int]$start -gt 0){$etag='"changed"'}
  $status=if($script:bad -eq 'status' -and [int]$start -gt 0){200}else{206}
  [IO.File]::WriteAllBytes($File,$data)
  [IO.File]::WriteAllText($Header,"HTTP/1.1 $status OK`r`nETag: $etag`r`nContent-Range: bytes $Range/$($script:bytes.Length)`r`n`r`n")
  if(-not $script:segmentCounts.ContainsKey($Range)){$script:segmentCounts[$Range]=0};$script:segmentCounts[$Range]++
  if($Range -ne '0-0' -and $script:segmentCounts[$Range] -eq 1){$code=35}
 }
 return [pscustomobject]@{process=[pscustomobject]@{ExitCode=$code};file=$File;header=$Header;range=$Range}
}
function Wait-DACurl($Task){return $Task.process.ExitCode}
try{
 $r=Invoke-DADependency $fixture 'https://repo.anaconda.com/miniconda/fixed.exe' 'good.exe' $digest 8
 Assert ($r.state -eq 'saved') 'Range fallback saved verified bytes'
 Assert ((Get-FileHash -LiteralPath (Join-Path $fixture 'good.exe')).Hash -eq $digest) 'Full SHA verified'
 Assert (@($script:segmentCounts.Values|Where-Object {$_ -gt 2}).Count -eq 0) 'At most one segment retry'
 $script:bad='etag';$script:segmentCounts=@{}
 Reject {Invoke-DADependency $fixture 'https://repo.anaconda.com/miniconda/fixed.exe' 'bad.exe' $digest 4}
 Assert (-not(Test-Path -LiteralPath (Join-Path $fixture 'bad.exe'))) 'Changed origin not published'
 $script:bad='status';$script:segmentCounts=@{}
 Reject {Invoke-DADependency $fixture 'https://repo.anaconda.com/miniconda/fixed.exe' 'bad-status.exe' $digest 4}
 Reject {Invoke-DADependency $fixture 'https://evil.example/file' 'bad-origin.exe' $digest 4}
 Reject {Invoke-DADependency $fixture 'https://repo.anaconda.com/miniconda/fixed.exe?token=x' 'bad-query.exe' $digest 4}
 [IO.File]::WriteAllText((Join-Path $fixture 'good.exe'),'changed by user')
 Reject {Clear-DADependency $fixture $r.id}
 Assert (Test-Path -LiteralPath (Join-Path $fixture 'good.exe')) 'Changed output retained'
 @{passed=$true;assertions=$script:count;scope='mock curl; Range validation, failed-segment retry and ownership';ps=$PSVersionTable.PSVersion.ToString()}|ConvertTo-Json
}finally{
 $resolved=[IO.Path]::GetFullPath($fixture);$tmp=[IO.Path]::GetFullPath($env:TEMP).TrimEnd('\')+'\'
 if(-not $resolved.StartsWith($tmp,[StringComparison]::OrdinalIgnoreCase) -or (Split-Path $resolved -Leaf) -notlike 'da-range-*'){throw 'Unsafe fixture cleanup path'}
 Remove-Item -LiteralPath $resolved -Recurse -Force
}

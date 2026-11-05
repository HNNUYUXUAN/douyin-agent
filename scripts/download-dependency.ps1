# No Python required. Downloads only verified official Windows dependency artifacts.
param([string]$Workspace,[string]$Url,[string]$Output,[string]$Sha256,[ValidateRange(1,8)][int]$Segments=8,[switch]$Cleanup)
$ErrorActionPreference='Stop'
. (Join-Path $PSScriptRoot 'discovery.ps1')
function Read-DAHeaders([string]$Path){
 if(-not (Test-Path -LiteralPath $Path)){return @{'_status'=0}}
 $text=[IO.File]::ReadAllText($Path);if($text -notmatch '(?m)^HTTP/\S+ \d{3}'){return @{'_status'=0}}
 $block=($text -split '(?m)^HTTP/\S+ ')[-1];$fields=@{'_status'=[int]($block.Substring(0,3))}
 foreach($line in @($block -split '\r?\n' | Select-Object -Skip 1)){if($line.Contains(':')){$key,$value=$line -split ':',2;$fields[$key.Trim().ToLower()]=$value.Trim()}}
 return $fields
}
function Start-DACurl([string]$Url,[string]$File,[string]$Header,[string]$Range,[string]$Validator){
 $exe=(Get-Command curl.exe -CommandType Application -ErrorAction Stop | Select-Object -First 1).Source
 $args=@('--disable','--silent','--show-error','--location','--proto','=https','--proto-redir','=https','--max-redirs','5','--connect-timeout','30','--max-time','300','--speed-limit','65536','--speed-time','30','--output',$File,'--dump-header',$Header)
 if($Range){$args+=@('--range',$Range)}
 if($Validator){$args+=@('--header',"If-Range: $Validator")}
 $args+=@('--url',$Url)
 # Official dependency URLs contain no query credentials; paths are quoted as native argv.
 $quoted=@($args | ForEach-Object {'"'+$_.Replace('"','\"')+'"'})
 $process=Start-Process -FilePath $exe -ArgumentList $quoted -WindowStyle Hidden -PassThru -RedirectStandardError ($Header+'.error')
 $null=$process.Handle
 return [pscustomobject]@{process=$process;file=$File;header=$Header;range=$Range}
}
function Wait-DACurl($Task){
 $watch=[Diagnostics.Stopwatch]::StartNew();$next=15
 while(-not $Task.process.WaitForExit(1000)){
  if($watch.Elapsed.TotalSeconds -ge $next){Write-Host (@{event='progress';stage='dependency_transfer';seconds=[int]$watch.Elapsed.TotalSeconds}|ConvertTo-Json -Compress);$next+=15}
 }
 $Task.process.WaitForExit();$Task.process.Refresh()
 if($null -eq $Task.process.ExitCode){throw 'Native curl exit code unavailable; preserve receipt'}
 return [int]$Task.process.ExitCode
}
function Invoke-DADependency([string]$Workspace,[string]$Url,[string]$Output,[string]$Sha256,[int]$Segments){
 $w=Assert-DAPlain $Workspace;$uri=[uri]$Url
 if($uri.Scheme -ne 'https' -or $uri.UserInfo -or $uri.Query -or $uri.Fragment){throw 'Use a clean official HTTPS dependency URL'}
 $allowed=$uri.Host -in @('repo.anaconda.com','gyan.dev','www.gyan.dev') -or ($uri.Host -eq 'github.com' -and $uri.AbsolutePath.StartsWith('/BtbN/FFmpeg-Builds/releases/'))
 if(-not $allowed -or $Sha256 -notmatch '^[a-fA-F0-9]{64}$'){throw 'Official-listed origin and expected SHA256 required'}
 if([IO.Path]::IsPathRooted($Output)){throw 'Use workspace-relative output'}
 $target=Assert-DAPlain (Join-Path $w $Output)
 if(-not $target.StartsWith($w.TrimEnd('\')+'\',[StringComparison]::OrdinalIgnoreCase) -or (Test-Path -LiteralPath $target)){throw 'Output must be new and inside workspace'}
 $id=[guid]::NewGuid().ToString('N').Substring(0,12);$dir=Join-Path $w "out\dependency\$id";$null=New-Item -ItemType Directory -Path $dir
 $receipt=Join-Path $w "out\dependency\$id.json";$record=@{id=$id;state='transferring';sha256_expected=$Sha256;owned_artifacts=@();at=[DateTimeOffset]::UtcNow.ToString('o')}
 try{
  $whole=Join-Path $dir 'whole.part';$hp=Join-Path $dir 'whole.headers'
  $task=Start-DACurl $Url $whole $hp '' ''; $code=Wait-DACurl $task
  $h=Read-DAHeaders $hp
  $record.whole_exit_code=$code;$record.http_status=$h['_status']
  if($code -ne 0){
   $probe=Join-Path $dir 'probe.part';$ph=Join-Path $dir 'probe.headers';$task=Start-DACurl $Url $probe $ph '0-0' ''
   if((Wait-DACurl $task) -ne 0){throw 'Range probe failed'}
   $h=Read-DAHeaders $ph
   if($h['_status'] -ne 206 -or $h['content-range'] -notmatch '^bytes 0-0/(\d+)$' -or (Get-Item -LiteralPath $probe).Length -ne 1){throw 'No validated Range support'}
   [long]$total=$Matches[1];$validator=$h['etag'];$key='etag'
   if(-not $validator -or $validator.StartsWith('W/')){$validator=$h['last-modified'];$key='last-modified'}
   if(-not $validator){throw 'No stable resource validator'}
   [long]$size=[math]::Ceiling($total/[double]$Segments);$tasks=@();$index=0
   for([long]$start=0;$start -lt $total;$start+=$size){
    $end=[math]::Min($total-1,$start+$size-1);$file=Join-Path $dir "p$index.part";$header=Join-Path $dir "p$index.headers"
    $tasks+=Start-DACurl $Url $file $header "$start-$end" $validator;$index++
   }
   foreach($item in $tasks){
    $rc=Wait-DACurl $item
    if($rc -in @(7,18,28,35,52,56)){$item2=Start-DACurl $Url $item.file $item.header $item.range $validator;$rc=Wait-DACurl $item2}
    if($rc -ne 0){throw 'Range segment failed after bounded retry'}
    $start,$end=$item.range -split '-';$f=Read-DAHeaders $item.header
    if($f['_status'] -ne 206 -or $f['content-range'] -ne "bytes $start-$end/$total" -or $f[$key] -ne $validator -or (Get-Item -LiteralPath $item.file).Length -ne ([long]$end-[long]$start+1)){throw 'Range length/identity mismatch'}
   }
   $merged=Join-Path $dir 'merged.part';$dst=[IO.File]::Open($merged,[IO.FileMode]::CreateNew)
   try{foreach($item in $tasks){$src=[IO.File]::OpenRead($item.file);try{$src.CopyTo($dst)}finally{$src.Dispose()}}}finally{$dst.Dispose()};$whole=$merged
  }
  elseif($h['_status'] -ne 200){throw 'Dependency HTTP response was not 200'}
  if((Get-FileHash -LiteralPath $whole -Algorithm SHA256).Hash -ne $Sha256){throw 'Complete dependency SHA256 mismatch'}
  $null=New-Item -ItemType Directory -Path (Split-Path $target -Parent) -Force
  [IO.File]::Move($whole,$target)
  $record.state='saved';$record.output=$target;$record.bytes=(Get-Item -LiteralPath $target).Length
  $record.owned_artifacts+=@{path=$target;sha256=$Sha256;created_by_task=$true}
 }catch{$record.state='failed';$record.error_type=$_.Exception.GetType().Name;$record.error_message=$_.Exception.Message;throw}
 finally{
  # Only these task-created curl children are awaited; no browser or user process is touched.
  foreach($item in @($tasks)){if($item){$null=Wait-DACurl $item}}
  foreach($p in @(Get-ChildItem -LiteralPath $dir -File)){
   if($p.Name -like '*.headers' -or $p.Name -like '*.error'){Remove-Item -LiteralPath $p.FullName}else{
    $item=@{path=$p.FullName;sha256=(Get-FileHash -LiteralPath $p.FullName -Algorithm SHA256).Hash;created_by_task=$true}
    if($record.state -eq 'saved'){Remove-Item -LiteralPath $p.FullName;$item.retired=$true}
    $record.owned_artifacts+= $item
   }
  }
  [IO.File]::WriteAllText($receipt,($record|ConvertTo-Json -Depth 8),[Text.UTF8Encoding]::new($false))
 }
 return $record
}
function Clear-DADependency([string]$Workspace,[string]$Id){
 if($Id -notmatch '^[a-f0-9]{12}$'){throw 'Invalid dependency transfer id'}
 $w=Assert-DAPlain $Workspace;$path=Join-Path $w "out\dependency\$Id.json";$r=Get-Content -Raw -Encoding UTF8 -LiteralPath $path|ConvertFrom-Json
 foreach($item in $r.owned_artifacts){
  $p=Assert-DAPlain $item.path
  if(-not $p.StartsWith($w.TrimEnd('\')+'\',[StringComparison]::OrdinalIgnoreCase)){throw 'Cleanup escaped workspace'}
  if(Test-Path -LiteralPath $p){if((Get-FileHash -LiteralPath $p -Algorithm SHA256).Hash -ne $item.sha256){throw 'Changed artifact retained'};Remove-Item -LiteralPath $p}
 }
 return @{status='owned_files_cleaned';id=$Id;receipt_retained=$true}
}
if($MyInvocation.InvocationName -ne '.'){
 if($Cleanup){Clear-DADependency $Workspace $Output|ConvertTo-Json}else{Invoke-DADependency $Workspace $Url $Output $Sha256 $Segments|ConvertTo-Json -Depth 8}
}

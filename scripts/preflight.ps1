param([Parameter(Mandatory=$true)][string]$Workspace,[string]$SkillDir,[string]$Conda,
 [ValidateSet('codex','workbuddy')][string]$TargetHost='workbuddy',
 [ValidateSet('zh-CN','en')][string]$Language='zh-CN')
$ErrorActionPreference='Stop'
. (Join-Path $PSScriptRoot 'discovery.ps1')
$root=Split-Path $PSScriptRoot -Parent
$version=(Get-Content -Raw -Encoding UTF8 -LiteralPath (Join-Path $root 'delivery.json') | ConvertFrom-Json).version
$w=Assert-DAPlain $Workspace
$terminal=Get-DATerminal
$found=Get-DAConda $Conda $w
$baseVersion=$null
if($found){
 $prior=$ErrorActionPreference
 try{$ErrorActionPreference='Continue';$baseVersion=& $found --version; $code=$LASTEXITCODE}finally{$ErrorActionPreference=$prior}
 if($code -ne 0){$baseVersion=$null}
}
$basePython=$null
if($found){
 $baseExe=Join-Path (Split-Path (Split-Path $found -Parent) -Parent) 'python.exe'
 if(Test-Path -LiteralPath $baseExe){$basePython=& $baseExe -B -c 'import sys; print(sys.version.split()[0])';if($LASTEXITCODE -ne 0){$basePython=$null}}
}
if(-not $SkillDir){
 $ctx=Join-Path $w 'workspace.json'
 if(Test-Path -LiteralPath $ctx){
  $saved=Get-Content -Raw -Encoding UTF8 -LiteralPath $ctx | ConvertFrom-Json
  $priorParts=@($saved.skill_root -split '[\\/]')
  $incompatible=if($TargetHost -eq 'workbuddy'){$priorParts -contains '.codex'}else{($priorParts -contains '.workbuddy') -or ($priorParts -contains '.codebuddy')}
  if(-not $incompatible){$SkillDir=$saved.skill_root}
 }
 if(-not $SkillDir){$SkillDir=Join-Path $env:USERPROFILE ".$TargetHost\skills\douyin-agent"}
}
$skill=Assert-DAPlain $SkillDir
$runtime=Join-Path $w 'envs\runtime\python.exe'
$pythonVersion=$null
if(Test-Path -LiteralPath $runtime){$pythonVersion=& $runtime -B -c 'import sys; print(sys.version.split()[0])';if($LASTEXITCODE -ne 0){$pythonVersion=$null}}
$tools=@{}
foreach($name in @('ffmpeg','ffprobe')){
 $local=Join-Path $w "tools\ffmpeg\bin\$name.exe"
 if(Test-Path -LiteralPath $local){$tools[$name]=Assert-DAPlain $local}else{
  $cmd=Get-Command $name -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1
  $tools[$name]=if($cmd){$cmd.Source}else{$null}
 }
}
$receiptPath=Join-Path $skill 'installed.json';$receipt=$null
if(Test-Path -LiteralPath $receiptPath){$data=Get-Content -Raw -Encoding UTF8 -LiteralPath $receiptPath | ConvertFrom-Json;$receipt=@{version=$data.version;workspace=$data.workspace}}
$missing=@()
if(-not $found -or -not $baseVersion){$missing+='conda'}
elseif(-not $basePython -or [version]$basePython -lt [version]'3.10'){$missing+='conda_base_python310'}
foreach($name in @('ffmpeg','ffprobe')){if(-not $tools[$name]){$missing+=$name}}
$index=Get-Content -Raw -Encoding UTF8 -LiteralPath (Join-Path $root 'docs\agent\index.json') | ConvertFrom-Json
$docs=@($index.setup_flow.required_docs.$Language | ForEach-Object {$_.Replace('{host}',$TargetHost)})
$ancestor=$w
while(-not(Test-Path -LiteralPath $ancestor)){$ancestor=Split-Path $ancestor -Parent;if(-not $ancestor){throw 'No workspace ancestor exists'}}
$aclWritable='unverified' # ACL inspection cannot establish effective write permission without writing.
$receiptMatches=($receipt -and $receipt.workspace -and $receipt.version -eq $version -and [IO.Path]::GetFullPath($receipt.workspace) -eq $w)
$arch=if($env:PROCESSOR_ARCHITEW6432){$env:PROCESSOR_ARCHITEW6432}else{$env:PROCESSOR_ARCHITECTURE}
$diskFree=$null
try{$drive=New-Object IO.DriveInfo([IO.Path]::GetPathRoot($w));$diskFree=$drive.AvailableFreeSpace}catch{}
[ordered]@{schema_version=1;flow='setup';observed_at=[DateTimeOffset]::UtcNow.ToString('o');
 os_version=[Environment]::OSVersion.Version.ToString();architecture=$arch;available_bytes=$diskFree;host_session_dir=(Get-Location).Path;
 architecture_supported=($arch -eq 'AMD64');
 workspace=$w;workspace_exists=(Test-Path -LiteralPath $w -PathType Container);workspace_write=$aclWritable;
 workspace_path_supported=($w.Length -le 85);skill_dir=$skill;installation=$receipt;
 terminal=$terminal;conda=@{executable=$found;version=(@($baseVersion) -join ' ');base_python_version=$basePython};
 python=@{executable=$runtime;version=$pythonVersion};media_tools=$tools;missing_dependencies=$missing;
 requested_version=$version;installation_matches=[bool]$receiptMatches;
 next_action=$(if($arch -ne 'AMD64'){'unsupported_architecture'}elseif($w.Length -gt 85){'choose_short_workspace'}elseif($missing.Count){'prepare_missing_dependencies'}elseif(-not $receiptMatches){'install_skill'}elseif(-not $pythonVersion -or [version]$pythonVersion -lt [version]'3.12' -or [version]$pythonVersion -ge [version]'3.13'){'repair_runtime'}else{'run_onboard_check'});
 required_docs=$docs;waiting_for=$null;browser_verified=$false;cloud_verified=$false;
 note='Read-only. Effective write permission is unverified; the installer checks writes. No environment dump, credential read or network request.'} | ConvertTo-Json -Depth 8

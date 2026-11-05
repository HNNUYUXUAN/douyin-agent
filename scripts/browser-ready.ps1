param([ValidateSet('Chrome','Edge')][string]$Browser='Chrome',[ValidateSet('Check','Launch')][string]$Mode='Check')
$ErrorActionPreference='Stop'
function Find-DABrowserExecutable([string]$Browser){
$name=if($Browser -eq 'Chrome'){'chrome.exe'}else{'msedge.exe'}
$paths=@()
foreach($hive in @('HKCU:','HKLM:')){
 $key="$hive\Software\Microsoft\Windows\CurrentVersion\App Paths\$name"
 if(Test-Path -LiteralPath $key){$paths+=(Get-Item -LiteralPath $key).GetValue('')}
}
foreach($base in @($env:ProgramFiles,${env:ProgramFiles(x86)},$env:LOCALAPPDATA)){
 if($base){$paths+=Join-Path $base $(if($Browser -eq 'Chrome'){'Google\Chrome\Application\chrome.exe'}else{'Microsoft\Edge\Application\msedge.exe'})}
}
return $paths | Where-Object {$_ -and (Test-Path -LiteralPath $_ -PathType Leaf)} | Select-Object -First 1
}
function Test-DABrowserRunning([string]$Browser){
$name=if($Browser -eq 'Chrome'){'chrome'}else{'msedge'}
return (@(Get-Process -Name $name -ErrorAction SilentlyContinue).Count -gt 0)
}
function Get-DABrowserReady([string]$Browser,[string]$Mode){
if($Browser -notin @('Chrome','Edge') -or $Mode -notin @('Check','Launch')){throw 'Use Chrome/Edge and Check/Launch'}
$exe=Find-DABrowserExecutable $Browser;$running=Test-DABrowserRunning $Browser
$launched=$false
if($Mode -eq 'Launch' -and -not $running){
 if(-not $exe){throw 'Selected browser installation not found'}
 # This is the user's interactive browser for handoff, not a background helper.
 $null=Start-Process -FilePath $exe -WindowStyle Normal
 $launched=$true
}
@{browser=$Browser;installed=[bool]$exe;running_before=$running;launched=$launched;connection='unverified';
 next_action='Inventory host extension instances; do not infer connection from process or registry';profile_data_read=$false}
}
if($MyInvocation.InvocationName -ne '.'){Get-DABrowserReady $Browser $Mode|ConvertTo-Json}

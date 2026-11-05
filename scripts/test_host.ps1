# Isolated process fixtures: no real browser starts, credential or registry writes.
$ErrorActionPreference='Stop'
. (Join-Path $PSScriptRoot 'browser-ready.ps1')
. (Join-Path $PSScriptRoot 'workbuddy-bridge.ps1')
$script:count=0;$script:starts=0;$script:running=$false;$script:installed=$true
function Assert($Value,[string]$Message){if(-not $Value){throw $Message};$script:count++}
function Find-DABrowserExecutable($Browser){if($script:installed){return 'C:\fixture\chrome.exe'}}
function Test-DABrowserRunning($Browser){return $script:running}
function Start-Process{param($FilePath,$WindowStyle);Assert ($WindowStyle -eq 'Normal') 'Interactive user browser is visible';$script:starts++}
$r=Get-DABrowserReady 'Chrome' 'Check';Assert (-not $r.running_before -and -not $r.launched) 'Stopped state is distinct'
$r=Get-DABrowserReady 'Chrome' 'Launch';Assert ($r.launched -and $script:starts -eq 1) 'Launch only selected stopped browser'
Assert ($r.connection -eq 'unverified' -and -not $r.profile_data_read) 'Process does not prove connection'
$script:running=$true;$r=Get-DABrowserReady 'Chrome' 'Launch';Assert (-not $r.launched -and $script:starts -eq 1) 'Running browser reused'
$script:running=$false;$script:installed=$false;$blocked=$false;try{Get-DABrowserReady 'Chrome' 'Launch'|Out-Null}catch{$blocked=$true};Assert $blocked 'Missing executable hands off'
Assert ((@(Normalize-Browser @('Chrome','Edge')) -join ',') -eq 'Chrome,Edge') 'Native array'
Assert ((@(Normalize-Browser @('Chrome,Edge')) -join ',') -eq 'Chrome,Edge') 'File comma string'
$blocked=$false;try{Normalize-Browser @('Chrome,IAB')|Out-Null}catch{$blocked=$true};Assert $blocked 'Strict browser enumeration'
@{passed=$true;assertions=$script:count;scope='mock browser launch; array normalization';ps=$PSVersionTable.PSVersion.ToString()}|ConvertTo-Json

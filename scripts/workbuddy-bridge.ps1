# Windows-only repair of an existing WorkBuddy browser bridge. See wiki runbook.
[CmdletBinding()]
param(
    [ValidateSet('Check','Plan','Repair','Rollback')][string]$Mode='Check',
    [string[]]$Browser=@(),
    [string]$WorkBuddyVersion,
    [string[]]$ExtensionId=@(),
    [string]$Root=(Join-Path $env:USERPROFILE '.workbuddy'),
    [string]$Receipt
)
$ErrorActionPreference='Stop'
function Normalize-Browser($Values){
    $result=@($Values | ForEach-Object {$_ -split ','} | ForEach-Object {$_.Trim()} | Select-Object -Unique)
    foreach($value in $result){if($value -notin @('Chrome','Edge')){throw 'Browser must be Chrome or Edge'}}
    return $result
}
$Browser=@(Normalize-Browser $Browser)
if($PSVersionTable.PSVersion.Major -eq 5){
    # Resolve Windows PowerShell modules locally when a PS7 parent supplied PSModulePath.
    foreach($module in @('Microsoft.PowerShell.Utility','Microsoft.PowerShell.Security')){
        Import-Module (Join-Path $PSHOME "Modules\$module\$module.psd1") -Force -ErrorAction Stop
    }
}
$Feed='https://static.workbuddy.cn/browser-computer-use/v1/browser-use/version.json'
$ApprovedIds=@('kkjblpnnljnmbhaaakgcmfioipgamgii','ajnnogdfpilbhkeggdjlcokgglijmdde','ndbfelmlimfjklodckmbalfioaehegpc')

function Safe-Path([string]$Path) {
    if (-not [IO.Path]::IsPathRooted($Path)) { throw 'Use an absolute path' }
    $full=[IO.Path]::GetFullPath($Path)
    $part=$full
    while ($part) {
        if (Test-Path -LiteralPath $part) {
            $item=Get-Item -LiteralPath $part -Force
            if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'Linked repair paths unsupported' }
        }
        $parent=[IO.Path]::GetDirectoryName($part)
        if ($parent -eq $part) { break }; $part=$parent
    }
    return $full
}
function Child-Path([string]$Parent,[string]$Relative) {
    $base=Safe-Path $Parent; $target=Safe-Path (Join-Path $base $Relative)
    if (-not $target.StartsWith($base.TrimEnd('\')+'\',[StringComparison]::OrdinalIgnoreCase)) { throw 'Repair target escaped root' }
    return $target
}
function Json-Read([string]$Path) {
    if (Test-Path -LiteralPath $Path) { return (Get-Content -LiteralPath $Path -Raw -Encoding UTF8 | ConvertFrom-Json) }
    return [pscustomobject]@{}
}
function Set-Field($Object,[string]$Name,$Value) {
    $Object | Add-Member -NotePropertyName $Name -NotePropertyValue $Value -Force
}
function Json-Write([string]$Path,$Value) {
    $null=Safe-Path $Path
    if ($script:WriteGuards -and $script:WriteGuards.ContainsKey($Path) -and (Fingerprint $Path) -ne $script:WriteGuards[$Path]) { throw 'Configuration changed during repair; preserved latest file' }
    $parent=Split-Path $Path -Parent; $null=New-Item -ItemType Directory -Path $parent -Force
    $tmp=$Path+'.'+[guid]::NewGuid().ToString('N')+'.tmp'
    try {
        [IO.File]::WriteAllText($tmp,($Value|ConvertTo-Json -Depth 100),[Text.UTF8Encoding]::new($false))
        Move-Item -LiteralPath $tmp -Destination $Path -Force
        if ($script:WriteGuards -and $script:WriteGuards.ContainsKey($Path)) { $script:WriteGuards[$Path]=Fingerprint $Path }
        if ($script:WriteRows -and $script:WriteRows.ContainsKey($Path)) { $script:WriteRows[$Path].modified=$true; $script:WriteRows[$Path].after=Fingerprint $Path }
    } finally { if (Test-Path -LiteralPath $tmp) { Remove-Item -LiteralPath $tmp } }
}
function Fingerprint([string]$Path) {
    if (-not (Test-Path -LiteralPath $Path)) { return 'absent' }
    $null=Safe-Path $Path
    $files=@(Get-Item -LiteralPath $Path -Force)
    if ($files[0].PSIsContainer) { $files=@(Get-ChildItem -LiteralPath $Path -Recurse -Force | Sort-Object FullName) }
    $lines=@($files | ForEach-Object {
        $null=Safe-Path $_.FullName
        if ($_.PSIsContainer) { 'D:'+ $_.FullName.Substring($Path.Length) }
        else { $_.FullName.Substring($Path.Length)+':'+(Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash }
    })
    $sha=[Security.Cryptography.SHA256]::Create()
    try { return ([BitConverter]::ToString($sha.ComputeHash([Text.Encoding]::UTF8.GetBytes(($lines -join "`n"))))).Replace('-','').ToLower() }
    finally { $sha.Dispose() }
}
function Registry-Key([string]$Family) {
    $vendor=if ($Family -eq 'Chrome') {'Google\Chrome'} else {'Microsoft\Edge'}
    return 'HKCU:\Software\'+$vendor+'\NativeMessagingHosts\com.workbuddy.extension'
}
function Registry-Read([string]$Key) {
    if (Test-Path -LiteralPath $Key) { return [pscustomobject]@{exists=$true;value=(Get-Item -LiteralPath $Key).GetValue('')} }
    return [pscustomobject]@{exists=$false;value=$null}
}
function Registry-Write([string]$Key,$State) {
    if ($State.exists) { $null=New-Item -Path $Key -Force; Set-Item -LiteralPath $Key -Value $State.value }
    elseif (Test-Path -LiteralPath $Key) {
        $item=Get-Item -LiteralPath $Key
        if ($item.SubKeyCount -or $item.ValueCount -gt 1) { throw 'Registry key gained unrelated data; manual recovery required' }
        Remove-Item -LiteralPath $Key
    }
}
function Select-Runtime($Document,[string]$AppVersion) {
    $app=[version]$AppVersion
    if ($Document.schema -ne 1 -or $Document.plugin -ne 'browser-use') { throw 'Unknown runtime feed schema' }
    $matches=@($Document.platforms.'win32-x64' | Where-Object { [version]$_.minAppVersion -le $app } | Sort-Object { [version]$_.version } -Descending)
    if (-not $matches.Count) { throw 'No compatible Windows x64 runtime' }
    $entry=$matches[0]
    if ($entry.sha256 -notmatch '^[0-9a-fA-F]{64}$' -or $entry.version -notmatch '^\d+\.\d+\.\d+$') { throw 'Invalid feed entry' }
    $uri=[Uri]::new([Uri]$Feed,[string]$entry.url)
    if ($uri.Scheme -ne 'https' -or $uri.Host -ne 'static.workbuddy.cn' -or -not $uri.AbsolutePath.StartsWith('/browser-computer-use/v1/browser-use/win32-x64/') -or $uri.Query) { throw 'Runtime URL outside approved official feed' }
    return [pscustomobject]@{entry=$entry;url=$uri.AbsoluteUri}
}
function Extract-Runtime([string]$Archive,[string]$Destination) {
    Add-Type -AssemblyName System.IO.Compression
    Add-Type -AssemblyName System.IO.Compression.FileSystem
    $zip=[IO.Compression.ZipFile]::OpenRead($Archive)
    try {
        if ($zip.Entries.Count -gt 2000) { throw 'Unexpected runtime archive size' }
        [long]$total=0
        foreach ($entry in $zip.Entries) {
            $name=$entry.FullName.Replace('\','/'); $total+=$entry.Length
            if ($total -gt 100MB -or $name -notmatch '^(browser-use/|\.codebuddy-plugin/)' -or $name -notmatch '^[A-Za-z0-9_.@/-]+$' -or $name -match '(^|/)\.\.?(/|$)|:|^/' -or ($entry.ExternalAttributes -band 0x400) -ne 0 -or (($entry.ExternalAttributes -shr 16) -band 0xF000) -eq 0xA000) { throw 'Unsafe runtime archive entry' }
            foreach ($segment in $name.TrimEnd('/').Split('/')) {
                if ($segment.EndsWith('.') -or $segment -match '^(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(\.|$)') { throw 'Windows-unsafe runtime archive name' }
            }
            $target=Child-Path $Destination $name
            if ($name.EndsWith('/')) { $null=New-Item -ItemType Directory -Path $target -Force }
            else { $null=New-Item -ItemType Directory -Path (Split-Path $target -Parent) -Force; [IO.Compression.ZipFileExtensions]::ExtractToFile($entry,$target,$false) }
        }
    } finally { $zip.Dispose() }
}
function Bridge-Check([string]$Base,[string[]]$Families) {
    $hostPath=Child-Path $Base 'browser-runtime/native-host/browser-extension-native-host.exe'
    $manifestPath=Child-Path $Base 'browser-runtime/native-host/com.workbuddy.extension.json'
    $manifest=Json-Read $manifestPath
    $rows=@(foreach ($family in $Families) {
        $reg=Registry-Read (Registry-Key $family)
        [pscustomobject]@{family=$family;registry_present=$reg.exists;registry_matches=($reg.value -eq $manifestPath)}
    })
    $ids=@($manifest.allowed_origins | Where-Object { $_ } | ForEach-Object { $_ -replace '^chrome-extension://','' -replace '/$','' })
    $hostPresent=Test-Path -LiteralPath $hostPath
    $signature=if ($hostPresent) { [string](Get-AuthenticodeSignature -LiteralPath $hostPath).Status } else {'missing'}
    $settings=Json-Read (Child-Path $Base 'settings.json')
    $runtimePresent=Test-Path -LiteralPath (Child-Path $Base 'native-runtimes/browser-use/browser-use/bin/browser-mcp.exe')
    $idsMatch=if ($ExtensionId.Count) { @($ExtensionId|Where-Object { $_ -notin $ids }).Count -eq 0 } else { $null }
    return [pscustomobject]@{host_present=$hostPresent;runtime_present=$runtimePresent;plugin_enabled=($settings.enabledPlugins.'browser-use@workbuddy-browser-use' -eq $true);signature=$signature;manifest_present=(Test-Path -LiteralPath $manifestPath);manifest_path_matches=($manifest.path -eq $hostPath -and $manifest.name -eq 'com.workbuddy.extension' -and $manifest.type -eq 'stdio');manifest_ids=$ids;extension_ids_match=$idsMatch;browsers=$rows;browser_discovery='unverified';dom='unverified';screenshot='unverified';requires_host_verification=$true}
}
function Restore-Receipt($Data) {
    # Validate every target before any rollback mutation. Never overwrite later user edits.
    if (-not $Data.root -or -not @($Data.files).Count) { throw 'Empty or malformed repair receipt' }
    foreach ($row in $Data.files) {
        if ($row.PSObject.Properties['modified'] -and -not $row.modified) { continue }
        $target=Child-Path $Data.root $row.relative
        $backupBase=Child-Path $Data.root 'bridge-backups'
        $backupPath=Safe-Path $row.backup
        if (-not $backupPath.StartsWith($backupBase+'\',[StringComparison]::OrdinalIgnoreCase)) { throw 'Backup outside bridge backup root' }
        if ((Fingerprint $target) -ne $row.after) { throw 'Target changed since repair; rollback requires review' }
        if ($row.before -ne 'absent' -and (Fingerprint $row.backup) -ne $row.before) { throw 'Backup fingerprint mismatch' }
    }
    foreach ($row in $Data.registry) {
        if ($row.PSObject.Properties['modified'] -and -not $row.modified) { continue }
        if ($row.key -notin @((Registry-Key 'Chrome'),(Registry-Key 'Edge'))) { throw 'Unexpected rollback registry key' }
        if (((Registry-Read $row.key)|ConvertTo-Json -Compress) -ne ($row.after|ConvertTo-Json -Compress)) { throw 'Registry changed since repair' }
    }
    foreach ($row in $Data.files) {
        if ($row.PSObject.Properties['modified'] -and -not $row.modified) { continue }
        $target=Child-Path $Data.root $row.relative
        if (Test-Path -LiteralPath $target) { Remove-Item -LiteralPath $target -Recurse -Force }
        if ($row.before -ne 'absent') { Copy-Item -LiteralPath $row.backup -Destination $target -Recurse -Force }
    }
    foreach ($row in $Data.registry) { if (-not $row.PSObject.Properties['modified'] -or $row.modified) { Registry-Write $row.key $row.before } }
}

function Invoke-BridgeMaintenance {
$rootPath=Safe-Path $Root
if ($rootPath.TrimEnd('\') -eq ([IO.Path]::GetPathRoot($rootPath)).TrimEnd('\')) { throw 'Use a WorkBuddy directory rather than a drive root' }
if ($Mode -eq 'Check') { $families=if ($Browser.Count) {$Browser} else {@('Chrome','Edge')}; Bridge-Check $rootPath $families | ConvertTo-Json -Depth 8; return }
if (-not $Receipt) { throw 'Specify an absolute private receipt path for Plan/Repair/Rollback' }
$receiptPath=Safe-Path $Receipt
if ($receiptPath.StartsWith($rootPath.TrimEnd('\')+'\',[StringComparison]::OrdinalIgnoreCase)) { throw 'Keep the private receipt in workspace ops, outside the WorkBuddy directory' }
if ($Mode -eq 'Rollback') {
    $data=Json-Read $receiptPath
    if ($data.schema_version -ne 1 -or $data.root -ne $rootPath -or $data.status -notin @('repaired','failed')) { throw 'Receipt does not describe a repair of this root' }
    if (Test-Path -LiteralPath (Child-Path $rootPath 'bridge-repair.lock')) { throw 'Repair lock present; inspect interrupted/active repair first' }
    Restore-Receipt $data; $data.status='rolled_back'; Json-Write $receiptPath $data; $data | ConvertTo-Json -Depth 10; return
}
if (-not [Environment]::Is64BitOperatingSystem -or -not (Test-Path -LiteralPath $rootPath)) { throw 'Requires an initialized WorkBuddy on Windows x64' }
if (-not $Browser.Count) { throw 'Pass the observed browser families explicitly with -Browser' }
if (-not $WorkBuddyVersion) { throw 'Pass the actually observed WorkBuddy version' }
if (-not $ExtensionId.Count -or @($ExtensionId | Where-Object { $_ -notin $ApprovedIds }).Count) { throw 'Pass the observed approved WorkBuddy extension IDs' }
$feedDoc=Invoke-RestMethod -Uri $Feed -UseBasicParsing -TimeoutSec 30 -MaximumRedirection 0
$runtime=Select-Runtime $feedDoc $WorkBuddyVersion
$report=[pscustomobject]@{mode=$Mode;root=$rootPath;app_version=$WorkBuddyVersion;runtime_version=$runtime.entry.version;sha256=$runtime.entry.sha256;url=$runtime.url;browser=$Browser;extension_ids=$ExtensionId;check=(Bridge-Check $rootPath $Browser)}
if ($Mode -eq 'Plan') { $report | ConvertTo-Json -Depth 10; return }
if (Test-Path -LiteralPath $receiptPath) { throw 'Receipt already exists; inspect it or choose a new path' }
if ($report.check.host_present -and $report.check.runtime_present -and $report.check.plugin_enabled -and $report.check.signature -eq 'Valid' -and $report.check.manifest_path_matches -and $report.check.extension_ids_match -and -not @($report.check.browsers|Where-Object {-not $_.registry_matches}).Count) {
    [pscustomobject]@{status='already_registered';requires_host_verification=$true} | ConvertTo-Json; return
}
$backup=Child-Path $rootPath ('bridge-backups/'+[guid]::NewGuid().ToString('N'))
$temp=Child-Path $backup 'package'; $null=New-Item -ItemType Directory -Path $temp -Force
$null=New-Item -ItemType Directory -Path (Split-Path $receiptPath -Parent) -Force
$lockPath=Child-Path $rootPath 'bridge-repair.lock'
$lock=[IO.File]::Open($lockPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
$data=[pscustomobject]@{schema_version=1;status='prepared';stage='download';root=$rootPath;artifact_root=$backup;at=[DateTimeOffset]::UtcNow.ToString('o');runtime=$report;files=@();registry=@()}
try {
    $archive=Child-Path $temp 'runtime.zip'
    Invoke-WebRequest -Uri $runtime.url -OutFile $archive -UseBasicParsing -TimeoutSec 60 -MaximumRedirection 0
    if ((Get-FileHash -LiteralPath $archive -Algorithm SHA256).Hash.ToLower() -ne $runtime.entry.sha256.ToLower()) { throw 'Runtime SHA256 mismatch' }
    $data.stage='extract_and_verify'
    $extract=Child-Path $temp 'extracted'; Extract-Runtime $archive $extract
    $plugin=Child-Path $extract 'browser-use'
    if ((Json-Read (Child-Path $plugin '.codebuddy-plugin/plugin.json')).version -ne $runtime.entry.version) { throw 'Package version mismatch' }
    foreach ($binary in @('browser-mcp.exe','browser-extension-native-host.exe')) {
        $sig=Get-AuthenticodeSignature -LiteralPath (Child-Path $plugin ('bin/'+$binary))
        if ($sig.Status -ne 'Valid' -or $sig.SignerCertificate.Subject -notmatch 'Tencent') { throw 'Runtime publisher signature failed' }
    }
    $data.stage='snapshot'
    $relative=@('native-runtimes/browser-use',('plugins/cache/workbuddy-browser-use/browser-use/'+$runtime.entry.version),'browser-runtime/native-host','settings.json','plugins/installed_plugins.json','plugins/known_marketplaces.json','native-runtimes/state.json')
    foreach ($rel in $relative) {
        $target=Child-Path $rootPath $rel; $before=Fingerprint $target; $copy=Child-Path $backup ('files/'+$rel)
        if ($before -ne 'absent') { $null=New-Item -ItemType Directory -Path (Split-Path $copy -Parent) -Force; Copy-Item -LiteralPath $target -Destination $copy -Recurse -Force }
        $data.files+= [pscustomobject]@{relative=$rel;before=$before;backup=$copy;after=$before;modified=$false}
    }
    foreach ($family in $Browser) { $key=Registry-Key $family; $prior=Registry-Read $key; $data.registry+=[pscustomobject]@{key=$key;before=$prior;after=$prior;modified=$false} }
    Json-Write $receiptPath $data
    foreach ($row in $data.files) { if ((Fingerprint (Child-Path $rootPath $row.relative)) -ne $row.before) { throw 'Configuration changed during backup; no repair applied' } }
    foreach ($row in $data.registry) { if (((Registry-Read $row.key)|ConvertTo-Json -Compress) -ne ($row.before|ConvertTo-Json -Compress)) { throw 'Registry changed during backup; no repair applied' } }
    $script:WriteGuards=@{}; $script:WriteRows=@{}
    foreach ($row in $data.files) { if ($row.relative.EndsWith('.json')) { $target=Child-Path $rootPath $row.relative; $script:WriteGuards[$target]=$row.before; $script:WriteRows[$target]=$row } }
    $data.stage='apply'
    # Only the selected plugin/runtime records are merged into the existing JSON.
    $runtimeDir=Child-Path $rootPath $relative[0]; $cacheDir=Child-Path $rootPath $relative[1]
    foreach ($pair in @(@($extract,$runtimeDir),@($plugin,$cacheDir))) {
        $original=@($data.files | Where-Object { (Child-Path $rootPath $_.relative) -eq $pair[1] })[0]
        if ((Fingerprint $pair[1]) -ne $original.before) { throw 'Runtime changed during repair' }
        $original.modified=$true
        $null=New-Item -ItemType Directory -Path $pair[1] -Force
        Get-ChildItem -LiteralPath $pair[0] -Force | Copy-Item -Destination $pair[1] -Recurse -Force
        $original.after=Fingerprint $pair[1]
    }
    $key='browser-use@workbuddy-browser-use'; $stamp=[DateTimeOffset]::UtcNow.ToString('o')
    $settingsPath=Child-Path $rootPath 'settings.json'; $settings=Json-Read $settingsPath
    if (-not $settings.enabledPlugins) { Set-Field $settings 'enabledPlugins' ([pscustomobject]@{}) }
    Set-Field $settings.enabledPlugins $key $true; Json-Write $settingsPath $settings
    $installedPath=Child-Path $rootPath 'plugins/installed_plugins.json'; $installed=Json-Read $installedPath
    if (-not $installed.plugins) { Set-Field $installed 'plugins' ([pscustomobject]@{}) }
    Set-Field $installed.plugins $key @([pscustomobject]@{scope='user';installPath=$cacheDir;version=$runtime.entry.version;installedAt=$stamp;lastUpdated=$stamp}); Json-Write $installedPath $installed
    $marketsPath=Child-Path $rootPath 'plugins/known_marketplaces.json'; $markets=Json-Read $marketsPath
    Set-Field $markets 'workbuddy-browser-use' ([pscustomobject]@{manifestName='workbuddy-browser-use';type='directory';source=[pscustomobject]@{source='directory';path=$runtimeDir};installLocation=$runtimeDir;lastUpdated=$stamp}); Json-Write $marketsPath $markets
    $statePath=Child-Path $rootPath 'native-runtimes/state.json'; $state=Json-Read $statePath
    if (-not $state.marketplaces) { Set-Field $state 'marketplaces' ([pscustomobject]@{}) }
    Set-Field $state.marketplaces 'browser-use' ([pscustomobject]@{sha256=$runtime.entry.sha256;url=$runtime.entry.url;version=$runtime.entry.version;installedAt=$stamp}); Json-Write $statePath $state
    $hostDir=Child-Path $rootPath 'browser-runtime/native-host'
    $hostRow=@($data.files|Where-Object {$_.relative -eq 'browser-runtime/native-host'})[0]
    if ((Fingerprint $hostDir) -ne $hostRow.before) { throw 'Native host changed during repair' }
    $hostRow.modified=$true; $null=New-Item -ItemType Directory -Path $hostDir -Force
    $hostExe=Child-Path $hostDir 'browser-extension-native-host.exe'
    Copy-Item -LiteralPath (Child-Path $plugin 'bin/browser-extension-native-host.exe') -Destination $hostExe -Force
    $manifestPath=Child-Path $hostDir 'com.workbuddy.extension.json'; $manifest=Json-Read $manifestPath
    Set-Field $manifest 'name' 'com.workbuddy.extension'; Set-Field $manifest 'description' 'WorkBuddy browser extension relay'; Set-Field $manifest 'path' $hostExe; Set-Field $manifest 'type' 'stdio'
    $origins=@($manifest.allowed_origins | Where-Object { $_ })+@($ExtensionId|ForEach-Object {'chrome-extension://'+$_+'/'})
    Set-Field $manifest 'allowed_origins' @($origins|Select-Object -Unique); Json-Write $manifestPath $manifest
    $hostRow.after=Fingerprint $hostDir
    foreach ($row in $data.registry) {
        if (((Registry-Read $row.key)|ConvertTo-Json -Compress) -ne ($row.before|ConvertTo-Json -Compress)) { throw 'Registry changed during repair' }
        Registry-Write $row.key ([pscustomobject]@{exists=$true;value=$manifestPath}); $row.modified=$true; $row.after=Registry-Read $row.key
    }
    $data.stage='verify_registration'; $finalCheck=Bridge-Check $rootPath $Browser
    if (-not $finalCheck.runtime_present -or -not $finalCheck.plugin_enabled -or $finalCheck.signature -ne 'Valid' -or -not $finalCheck.manifest_path_matches -or -not $finalCheck.extension_ids_match -or @($finalCheck.browsers|Where-Object {-not $_.registry_matches}).Count) { throw 'Static bridge verification failed; inspect receipt and host checks' }
    $data.status='repaired'; $data.stage='host_verification_pending'
} catch {
    $data.status='failed'; $failure=$_.Exception.Message
    # Record the exact partial state. Recovery uses the same guarded rollback path.
    $data | Add-Member -NotePropertyName error -NotePropertyValue $failure -Force
    throw
} finally {
    Json-Write $receiptPath $data
    $lock.Dispose(); Remove-Item -LiteralPath (Safe-Path $lockPath)
}
$report.check=$finalCheck
[pscustomobject]@{status=$data.status;receipt=$receiptPath;check=$report.check;next='Re-enumerate host browsers; verify DOM and screenshot independently. No browser process was stopped.'} | ConvertTo-Json -Depth 10
}
# Dot sourcing exposes helpers for fixture tests without running maintenance.
if ($MyInvocation.InvocationName -ne '.') { Invoke-BridgeMaintenance }

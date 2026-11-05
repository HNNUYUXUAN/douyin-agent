$ErrorActionPreference='Stop'
. (Join-Path $PSScriptRoot 'workbuddy-bridge.ps1')
$fixture=Join-Path ([IO.Path]::GetFullPath($env:TEMP)) ('da-bridge-'+[guid]::NewGuid().ToString('N'))
$null=New-Item -ItemType Directory -Path $fixture
$count=0
function Assert($Condition,[string]$Message) { if (-not $Condition) { throw $Message }; $script:count++ }
function Reject([scriptblock]$Action) { $blocked=$false; try { & $Action } catch { $blocked=$true }; Assert $blocked 'Expected rejection' }
try {
    $feedDoc=[pscustomobject]@{schema=1;plugin='browser-use';platforms=[pscustomobject]@{'win32-x64'=@(
        [pscustomobject]@{version='2.0.0';minAppVersion='6.0.0';sha256=('a'*64);url='win32-x64/new.zip'},
        [pscustomobject]@{version='1.2.1';minAppVersion='5.6.0';sha256=('b'*64);url='win32-x64/old.zip'})}}
    Assert ((Select-Runtime $feedDoc '5.9.3').entry.version -eq '1.2.1') 'Must skip incompatible newest runtime'
    Reject { Select-Runtime $feedDoc '5.5.0' }
    $feedDoc.platforms.'win32-x64'[1].url='https://example.org/runtime.zip'
    Reject { Select-Runtime $feedDoc '5.9.3' }
    Reject { Child-Path $fixture '../escaped' }
    $path=Child-Path $fixture 'settings.json'
    Json-Write $path ([pscustomobject]@{untouched=[pscustomobject]@{deep=[pscustomobject]@{value='keep'}};enabledPlugins=[pscustomobject]@{'other@other'=$true}})
    $before=Fingerprint $path; $script:WriteGuards=@{}; $script:WriteGuards[$path]=$before
    $settings=Json-Read $path; Set-Field $settings.enabledPlugins 'browser-use@workbuddy-browser-use' $true
    Json-Write $path $settings
    Assert ((Json-Read $path).untouched.deep.value -eq 'keep') 'Preserve nested configuration'
    Assert ((Json-Read $path).enabledPlugins.'other@other') 'Preserve unrelated plugin'
    [IO.File]::WriteAllText($path,'{"latest":"user change"}')
    Reject { Json-Write $path $settings }
    Assert ((Json-Read $path).latest -eq 'user change') 'Preserve concurrent edit'
    $script:WriteGuards=@{}
    $backup=Child-Path $fixture 'bridge-backups/test/files/settings.json'
    $null=New-Item -ItemType Directory -Path (Split-Path $backup -Parent) -Force
    Copy-Item -LiteralPath $path -Destination $backup
    $original=Fingerprint $path; Json-Write $path ([pscustomobject]@{repaired=$true})
    $snapshotReceipt=[pscustomobject]@{root=$fixture;files=@([pscustomobject]@{relative='settings.json';backup=$backup;before=$original;after=(Fingerprint $path)});registry=@()}
    Restore-Receipt $snapshotReceipt
    Assert ((Json-Read $path).latest -eq 'user change') 'Rollback restored exact original'
    Reject { Restore-Receipt $snapshotReceipt }
    $archive=Child-Path $fixture 'unsafe.zip'
    Add-Type -AssemblyName System.IO.Compression
    Add-Type -AssemblyName System.IO.Compression.FileSystem
    $zip=[IO.Compression.ZipFile]::Open($archive,[IO.Compression.ZipArchiveMode]::Create)
    $entry=$zip.CreateEntry('browser-use/../../escape.exe'); $zip.Dispose()
    Reject { Extract-Runtime $archive (Child-Path $fixture 'extract') }
    # Native registry reads are mocked, so this suite cannot alter real browser registration.
    function Registry-Read([string]$Key) { return [pscustomobject]@{exists=$false;value=$null} }
    $check=Bridge-Check $fixture @('Chrome','Edge')
    Assert (-not $check.host_present) 'Missing runtime detected'
    Assert ($check.browsers.Count -eq 2 -and -not $check.browsers[0].registry_matches) 'Browsers checked separately'
    Assert ($check.screenshot -eq 'unverified') 'Registration never proves screenshots'
    Assert ($null -eq $check.extension_ids_match) 'Absent observed extension ID remains unknown'
    # Exercise the entire transaction with mock feed/signature/registry boundaries.
    $package=Child-Path $fixture 'fixture-package'; $plugin=Child-Path $package 'browser-use'
    $null=New-Item -ItemType Directory -Path (Child-Path $plugin 'bin') -Force
    [IO.File]::WriteAllText((Child-Path $plugin 'bin/browser-mcp.exe'),'fixture')
    [IO.File]::WriteAllText((Child-Path $plugin 'bin/browser-extension-native-host.exe'),'fixture')
    Json-Write (Child-Path $plugin '.codebuddy-plugin/plugin.json') ([pscustomobject]@{name='browser-use';version='1.2.1'})
    Json-Write (Child-Path $package '.codebuddy-plugin/marketplace.json') ([pscustomobject]@{name='workbuddy-browser-use'})
    $script:fixtureArchive=Child-Path $fixture 'valid.zip'
    [IO.Compression.ZipFile]::CreateFromDirectory($package,$script:fixtureArchive)
    $script:fixtureFeed=[pscustomobject]@{schema=1;plugin='browser-use';platforms=[pscustomobject]@{'win32-x64'=@([pscustomobject]@{version='1.2.1';minAppVersion='5.6.0';sha256=(Get-FileHash $script:fixtureArchive -Algorithm SHA256).Hash.ToLower();url='win32-x64/fixture.zip'})}}
    $script:fixtureRegistry=@{}
    function Invoke-RestMethod { return $script:fixtureFeed }
    function Invoke-WebRequest { param($Uri,$OutFile,[switch]$UseBasicParsing,$TimeoutSec,$MaximumRedirection); Copy-Item -LiteralPath $script:fixtureArchive -Destination $OutFile }
    $script:fixtureSignatureStatus='Valid'
    function Get-AuthenticodeSignature { return [pscustomobject]@{Status=$script:fixtureSignatureStatus;SignerCertificate=[pscustomobject]@{Subject='Tencent offline fixture'}} }
    function Registry-Read([string]$Key) {
        if ($script:fixtureRegistry.ContainsKey($Key)) { return $script:fixtureRegistry[$Key] }
        return [pscustomobject]@{exists=$false;value=$null}
    }
    function Registry-Write([string]$Key,$State) { $script:fixtureRegistry[$Key]=$State }
    $Root=Child-Path $fixture 'app';$null=New-Item -ItemType Directory -Path $Root
    Json-Write (Child-Path $Root 'settings.json') ([pscustomobject]@{untouched='keep';enabledPlugins=[pscustomobject]@{'other@other'=$true}})
    $originalSettings=Get-Content -LiteralPath (Child-Path $Root 'settings.json') -Raw
    $Receipt=Child-Path $fixture 'repair.json';$Mode='Repair';$Browser=@('Chrome','Edge');$WorkBuddyVersion='5.9.3';$ExtensionId=@('ajnnogdfpilbhkeggdjlcokgglijmdde')
    $result=Invoke-BridgeMaintenance | ConvertFrom-Json
    Assert ($result.status -eq 'repaired') 'Full fixture repair completed'
    Assert ($result.check.runtime_present -and $result.check.plugin_enabled) 'Plugin/runtime verified separately'
    Assert ((Json-Read (Child-Path $Root 'settings.json')).untouched -eq 'keep') 'Repair preserves unrelated settings'
    Assert ($result.check.browsers[0].registry_matches -and $result.check.browsers[1].registry_matches) 'Both fixture browser registrations verified'
    $savedReceipt=$Receipt;$Receipt=Child-Path $fixture 'unused.json'
    Assert ((Invoke-BridgeMaintenance|ConvertFrom-Json).status -eq 'already_registered') 'Repeated repair is idempotent'
    Assert (-not (Test-Path -LiteralPath $Receipt)) 'Idempotent repair creates no new receipt'
    $Mode='Rollback';$Receipt=$savedReceipt;$restored=Invoke-BridgeMaintenance | ConvertFrom-Json
    Assert ($restored.status -eq 'rolled_back') 'Full transaction rollback completed'
    Assert ((Get-Content -LiteralPath (Child-Path $Root 'settings.json') -Raw) -ceq $originalSettings) 'Exact original configuration bytes restored'
    Assert (-not (Test-Path -LiteralPath (Child-Path $Root 'browser-runtime/native-host'))) 'New native host directory removed on rollback'
    Assert (-not (Registry-Read (Registry-Key 'Chrome')).exists) 'Original registry absence restored'
    $Mode='Repair';$Receipt=Child-Path $fixture 'bad-hash.json'
    $script:fixtureFeed.platforms.'win32-x64'[0].sha256='0'*64
    Reject { Invoke-BridgeMaintenance }
    Assert ((Json-Read $Receipt).stage -eq 'download') 'Hash failure has a staged receipt'
    Assert ((Get-Content -LiteralPath (Child-Path $Root 'settings.json') -Raw) -ceq $originalSettings) 'Hash failure preserves configuration'
    $script:fixtureFeed.platforms.'win32-x64'[0].sha256=(Get-FileHash $script:fixtureArchive -Algorithm SHA256).Hash.ToLower()
    $Receipt=Child-Path $fixture 'bad-signature.json';$script:fixtureSignatureStatus='NotSigned'
    Reject { Invoke-BridgeMaintenance }
    Assert ((Json-Read $Receipt).stage -eq 'extract_and_verify') 'Signature failure has a staged receipt'
    Assert (-not (Test-Path -LiteralPath (Child-Path $Root 'browser-runtime/native-host'))) 'Invalid signature never installs a host'
    [pscustomobject]@{passed=$count;scope='offline fixtures; no live registry writes or runtime installation'} | ConvertTo-Json
} finally {
    $resolved=[IO.Path]::GetFullPath($fixture)
    $tempBase=[IO.Path]::GetFullPath($env:TEMP).TrimEnd('\')+'\'
    if ($resolved.StartsWith($tempBase,[StringComparison]::OrdinalIgnoreCase) -and (Split-Path $resolved -Leaf) -like 'da-bridge-*') { Remove-Item -LiteralPath $resolved -Recurse -Force }
}

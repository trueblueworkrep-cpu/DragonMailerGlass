# Dragon Mailer - Desktop Shortcut Creator
$AppPath = $PSScriptRoot
$ShortcutName = "Dragon Mailer"
$DesktopPath = [Environment]::GetFolderPath("Desktop")
$ShortcutPath = Join-Path $DesktopPath "$ShortcutName.lnk"

# Create WScript Shell object
$WshShell = New-Object -ComObject WScript.Shell

# Create shortcut
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = Join-Path $AppPath "DragonMailer.bat"
$Shortcut.WorkingDirectory = $AppPath
$Shortcut.Description = "Dragon Mailer - Bulk Email and SMS Application"
$Shortcut.WindowStyle = 1

# Set icon (use custom if exists, otherwise use default)
$IconPath = Join-Path $AppPath "images\dragon_logo.ico"
if (Test-Path $IconPath) {
    $Shortcut.IconLocation = "$IconPath,0"
} else {
    # Try PNG as fallback (some systems support it)
    $PngPath = Join-Path $AppPath "images\dragon_logo.png"
    if (Test-Path $PngPath) {
        $Shortcut.IconLocation = "$PngPath,0"
    }
}

$Shortcut.Save()

Write-Host "Desktop shortcut created: $ShortcutPath" -ForegroundColor Green

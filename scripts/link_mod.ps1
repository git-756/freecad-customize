# Link/unlink Mod\Customize into the FreeCAD user Mod folder (Windows).
# NOTE: not verified on Windows yet.
#
# Usage: scripts\link_mod.ps1 link|unlink|status [-ModDir <FreeCAD Mod folder>]
#   The Mod folder can also be given via the FREECAD_MOD_DIR environment variable.
#
# A directory junction is used instead of a symbolic link, so no administrator
# rights or Developer Mode are needed.
param(
    [Parameter(Position = 0, Mandatory = $true)]
    [ValidateSet('link', 'unlink', 'status')]
    [string]$Action,

    [Parameter(Position = 1)]
    [string]$ModDir = $env:FREECAD_MOD_DIR
)

$ErrorActionPreference = 'Stop'

$Name = 'Customize'
$RepoRoot = Split-Path -Parent $PSScriptRoot
$Src = Join-Path $RepoRoot "Mod\$Name"

if ([string]::IsNullOrWhiteSpace($ModDir)) {
    Write-Error @'
FreeCAD Mod folder is not specified.

Find the user data folder by running this in FreeCAD's Python console:
    App.getUserAppDataDir()
The Mod folder is the "Mod" directory inside it. Then run, e.g.:
    powershell -ExecutionPolicy Bypass -File scripts\link_mod.ps1 link "<user data dir>\Mod"
'@
    exit 1
}

$Dest = Join-Path $ModDir $Name

function Get-LinkTarget($path) {
    $item = Get-Item -LiteralPath $path -Force
    if ($item.LinkType -eq 'Junction' -or $item.LinkType -eq 'SymbolicLink') {
        return (@($item.Target)[0]).TrimEnd('\')
    }
    return $null
}

$exists = Test-Path -LiteralPath $Dest
$target = if ($exists) { Get-LinkTarget $Dest } else { $null }

switch ($Action) {
    'link' {
        if (-not (Test-Path -LiteralPath $Src -PathType Container)) {
            Write-Error "source not found: $Src"
            exit 1
        }
        if (-not (Test-Path -LiteralPath $ModDir -PathType Container)) {
            Write-Error "Mod folder does not exist: $ModDir"
            exit 1
        }
        if ($exists) {
            if ($target -and ($target -eq $Src.TrimEnd('\'))) {
                Write-Output "already linked: $Dest -> $Src"
                exit 0
            }
            if ($target) {
                Write-Error "$Dest is a link to a different target: $target"
            } else {
                Write-Error "$Dest already exists and is not a link; refusing to overwrite"
            }
            exit 1
        }
        New-Item -ItemType Junction -Path $Dest -Target $Src | Out-Null
        Write-Output "linked: $Dest -> $Src"
    }
    'unlink' {
        if ($exists -and $target) {
            # Delete only the link itself, never the contents of the target.
            [System.IO.Directory]::Delete($Dest, $false)
            Write-Output "unlinked: $Dest"
        } elseif ($exists) {
            Write-Error "$Dest is not a link; refusing to remove"
            exit 1
        } else {
            Write-Output "not linked: $Dest does not exist"
        }
    }
    'status' {
        if ($exists -and $target) {
            if ($target -eq $Src.TrimEnd('\')) {
                Write-Output "linked: $Dest -> $target"
            } else {
                Write-Output "link to a different target: $Dest -> $target"
            }
        } elseif ($exists) {
            Write-Output "exists but is not a link: $Dest"
        } else {
            Write-Output "not linked: $Dest does not exist"
        }
    }
}

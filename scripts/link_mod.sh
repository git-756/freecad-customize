#!/usr/bin/env bash
# Link/unlink Mod/Customize into the FreeCAD user Mod folder.
#
# Usage: scripts/link_mod.sh link|unlink|status [FREECAD_MOD_DIR]
#   FREECAD_MOD_DIR can also be given via the environment variable of the same name.
set -euo pipefail

NAME="Customize"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
SRC="$REPO_ROOT/Mod/$NAME"

usage() {
  echo "Usage: $0 link|unlink|status [FREECAD_MOD_DIR]" >&2
}

if [[ $# -lt 1 || $# -gt 2 ]]; then
  usage
  exit 1
fi

ACTION="$1"
MOD_DIR="${2:-${FREECAD_MOD_DIR:-}}"

if [[ -z "$MOD_DIR" ]]; then
  cat >&2 <<'MSG'
FreeCAD Mod folder is not specified.

Find the user data folder by running this in FreeCAD's Python console:
    App.getUserAppDataDir()
The Mod folder is the "Mod" directory inside it. Then run, e.g.:
    FREECAD_MOD_DIR="<user data dir>/Mod" scripts/link_mod.sh link
or pass it as the second argument:
    scripts/link_mod.sh link "<user data dir>/Mod"
MSG
  exit 1
fi

DEST="$MOD_DIR/$NAME"

case "$ACTION" in
  link)
    if [[ ! -d "$SRC" ]]; then
      echo "error: source not found: $SRC" >&2
      exit 1
    fi
    if [[ ! -d "$MOD_DIR" ]]; then
      echo "error: Mod folder does not exist: $MOD_DIR" >&2
      exit 1
    fi
    if [[ -L "$DEST" ]]; then
      if [[ "$(readlink "$DEST")" == "$SRC" ]]; then
        echo "already linked: $DEST -> $SRC"
        exit 0
      fi
      echo "error: $DEST is a symlink to a different target: $(readlink "$DEST")" >&2
      exit 1
    fi
    if [[ -e "$DEST" ]]; then
      echo "error: $DEST already exists and is not a symlink; refusing to overwrite" >&2
      exit 1
    fi
    ln -s "$SRC" "$DEST"
    echo "linked: $DEST -> $SRC"
    ;;
  unlink)
    if [[ -L "$DEST" ]]; then
      rm "$DEST"
      echo "unlinked: $DEST"
    elif [[ -e "$DEST" ]]; then
      echo "error: $DEST is not a symlink; refusing to remove" >&2
      exit 1
    else
      echo "not linked: $DEST does not exist"
    fi
    ;;
  status)
    if [[ -L "$DEST" ]]; then
      target="$(readlink "$DEST")"
      if [[ "$target" == "$SRC" ]]; then
        echo "linked: $DEST -> $target"
      else
        echo "symlink to a different target: $DEST -> $target"
      fi
    elif [[ -e "$DEST" ]]; then
      echo "exists but is not a symlink: $DEST"
    else
      echo "not linked: $DEST does not exist"
    fi
    ;;
  *)
    usage
    exit 1
    ;;
esac

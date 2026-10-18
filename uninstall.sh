#!/bin/sh
# uninstall.sh -- remove FICCWriting, the FICC writing skills, from PREFIX/.claude (default PREFIX: $HOME).
#
#   sh uninstall.sh [--prefix DIR] [--restore BACKUP_DIR]
#
# Removes PREFIX/.claude/skills/ficc-voice, PREFIX/.claude/skills/ficc-hand and the five
# agent cards in PREFIX/.claude/agents/.  With --restore, then moves the copies kept in
# BACKUP_DIR (a ficc-writing-backup-<UTC timestamp>/ made by install.sh) back into place
# and removes the emptied backup directory.
# Exit codes: 0 done; 2 usage error or a failed step.

set -u

SKILLS="ficc-voice ficc-hand"
CARDS="ficc-outliner ficc-structurer ficc-composer ficc-writer ficc-mapper"

usage() {
    sed -n '2,10p' "$0" | sed 's/^# \{0,1\}//'
}

die() {
    echo "uninstall.sh: $*" >&2
    exit 2
}

PREFIX=${HOME:-}
RESTORE=""
while [ $# -gt 0 ]; do
    case $1 in
        --prefix)
            [ $# -ge 2 ] || die "--prefix needs a directory"
            PREFIX=$2
            shift 2
            ;;
        --prefix=*)
            PREFIX=${1#--prefix=}
            shift
            ;;
        --restore)
            [ $# -ge 2 ] || die "--restore needs a backup directory"
            RESTORE=$2
            shift 2
            ;;
        --restore=*)
            RESTORE=${1#--restore=}
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            die "unknown argument: $1 (see --help)"
            ;;
    esac
done
[ -n "$PREFIX" ] || die "no prefix: HOME is unset and --prefix not given"
[ -d "$PREFIX" ] || die "no such directory: $PREFIX"
PREFIX=$(cd "$PREFIX" && pwd) || die "cannot enter $PREFIX"
DEST=$PREFIX/.claude

if [ -n "$RESTORE" ]; then
    [ -d "$RESTORE" ] || die "no such backup directory: $RESTORE"
    RESTORE=$(cd "$RESTORE" && pwd) || die "cannot enter $RESTORE"
    case $(basename "$RESTORE") in
        ficc-writing-backup-*) ;;
        *) die "not a backup made by install.sh: $RESTORE" ;;
    esac
    [ -d "$RESTORE/skills" ] || [ -d "$RESTORE/agents" ] || die "backup holds no skills/ or agents/: $RESTORE"
fi

# 1. Remove the installed files.
removed=0
for s in $SKILLS; do
    if [ -e "$DEST/skills/$s" ] || [ -L "$DEST/skills/$s" ]; then
        rm -rf "$DEST/skills/$s" || die "cannot remove $DEST/skills/$s"
        echo "Removed $DEST/skills/$s"
        removed=$((removed + 1))
    fi
done
for c in $CARDS; do
    if [ -e "$DEST/agents/$c.md" ] || [ -L "$DEST/agents/$c.md" ]; then
        rm -f "$DEST/agents/$c.md" || die "cannot remove $DEST/agents/$c.md"
        echo "Removed $DEST/agents/$c.md"
        removed=$((removed + 1))
    fi
done
[ "$removed" -gt 0 ] || echo "No FICCWriting files installed under $DEST"

# 2. Restore a backup.
if [ -n "$RESTORE" ]; then
    restored=0
    for s in $SKILLS; do
        if [ -e "$RESTORE/skills/$s" ] || [ -L "$RESTORE/skills/$s" ]; then
            mkdir -p "$DEST/skills" || die "cannot create $DEST/skills"
            mv "$RESTORE/skills/$s" "$DEST/skills/$s" || die "cannot restore skills/$s"
            echo "Restored $DEST/skills/$s"
            restored=$((restored + 1))
        fi
    done
    for c in $CARDS; do
        if [ -e "$RESTORE/agents/$c.md" ] || [ -L "$RESTORE/agents/$c.md" ]; then
            mkdir -p "$DEST/agents" || die "cannot create $DEST/agents"
            mv "$RESTORE/agents/$c.md" "$DEST/agents/$c.md" || die "cannot restore agents/$c.md"
            echo "Restored $DEST/agents/$c.md"
            restored=$((restored + 1))
        fi
    done
    rmdir "$RESTORE/skills" "$RESTORE/agents" 2>/dev/null
    if rmdir "$RESTORE" 2>/dev/null; then
        echo "Restored $restored item(s); removed the empty backup $RESTORE"
    else
        echo "Restored $restored item(s); $RESTORE still holds other files and was kept"
    fi
fi
exit 0

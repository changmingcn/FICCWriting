#!/bin/sh
# install.sh -- install FICCWriting, the FICC writing skills, into PREFIX/.claude (default PREFIX: $HOME).
#
#   sh install.sh [--prefix DIR]
#
# Copies skills/ficc-voice and skills/ficc-hand into PREFIX/.claude/skills/ and the five
# agent cards into PREFIX/.claude/agents/.  Existing copies are first moved to
# PREFIX/.claude/ficc-writing-backup-<UTC timestamp>/ and the restore command is printed.
# After installing, runs the self-tests in the installed tree; exits 1 if any fails.
# Exit codes: 0 installed and all self-tests passed; 1 a self-test failed; 2 usage or
# environment error (nothing installed).

set -u

SKILLS="ficc-voice ficc-hand"
CARDS="ficc-outliner ficc-structurer ficc-composer ficc-writer ficc-mapper"

usage() {
    sed -n '2,11p' "$0" | sed 's/^# \{0,1\}//'
}

die() {
    echo "install.sh: $*" >&2
    exit 2
}

PREFIX=${HOME:-}
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

HERE=$(cd "$(dirname "$0")" && pwd) || die "cannot locate the release directory"
for s in $SKILLS; do
    [ -f "$HERE/skills/$s/SKILL.md" ] || die "missing $HERE/skills/$s/SKILL.md"
done
for c in $CARDS; do
    [ -f "$HERE/agents/$c.md" ] || die "missing $HERE/agents/$c.md"
done

command -v python3 >/dev/null 2>&1 || die "python3 not found (Python 3.9+ required)"
python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)' \
    || die "Python 3.9+ required, found $(python3 -V 2>&1)"

mkdir -p "$PREFIX" || die "cannot create $PREFIX"
PREFIX=$(cd "$PREFIX" && pwd) || die "cannot enter $PREFIX"
DEST=$PREFIX/.claude
case $HERE in
    "$DEST"/skills/*|"$DEST"/agents/*) die "run install.sh from the release directory, not from inside $DEST" ;;
esac

# 1. Back up existing copies.
existing=""
for s in $SKILLS; do
    if [ -e "$DEST/skills/$s" ] || [ -L "$DEST/skills/$s" ]; then
        existing="$existing skills/$s"
    fi
done
for c in $CARDS; do
    if [ -e "$DEST/agents/$c.md" ] || [ -L "$DEST/agents/$c.md" ]; then
        existing="$existing agents/$c.md"
    fi
done
if [ -n "$existing" ]; then
    TS=$(date -u +%Y%m%dT%H%M%SZ)
    BACKUP=$DEST/ficc-writing-backup-$TS
    n=1
    while [ -e "$BACKUP" ]; do
        BACKUP=$DEST/ficc-writing-backup-$TS-$n
        n=$((n + 1))
    done
    mkdir -p "$BACKUP/skills" "$BACKUP/agents" || die "cannot create $BACKUP"
    for item in $existing; do
        mv "$DEST/$item" "$BACKUP/$item" || die "cannot move $DEST/$item to $BACKUP/$item"
    done
    echo "Backed up existing copies:$existing"
    echo "  to $BACKUP"
    echo "Restore with: sh \"$HERE/uninstall.sh\" --prefix \"$PREFIX\" --restore \"$BACKUP\""
fi

# 2. Copy.
mkdir -p "$DEST/skills" "$DEST/agents" || die "cannot create $DEST/skills or $DEST/agents"
for s in $SKILLS; do
    cp -RP "$HERE/skills/$s" "$DEST/skills/$s" || die "copy failed: skills/$s"
done
for c in $CARDS; do
    cp "$HERE/agents/$c.md" "$DEST/agents/$c.md" || die "copy failed: agents/$c.md"
done
echo "Installed FICCWriting: skills ($SKILLS) and cards ($CARDS) into $DEST"

# 3. Self-tests in the installed tree.
V=$DEST/skills/ficc-voice/scripts
H=$DEST/skills/ficc-hand/scripts
fails=0
check() {
    label=$1
    shift
    out=$("$@" 2>&1)
    rc=$?
    last=$(printf '%s\n' "$out" | sed '/^[[:space:]]*$/d' | tail -n 1)
    if [ "$rc" -eq 0 ]; then
        echo "PASS  $label  | $last"
    else
        echo "FAIL  $label (exit $rc)  | $last"
        fails=$((fails + 1))
    fi
}
echo "Self-tests:"
check "xref_check.py -q"                 python3 -B "$V/xref_check.py" -q
check "xref_check.py --selftest"         python3 -B "$V/xref_check.py" --selftest
check "voice_check.py --selftest"        python3 -B "$V/voice_check.py" --selftest
check "voice_check.py --selftest --clarity" python3 -B "$V/voice_check.py" --selftest --clarity
check "tieout.py --self-test"            python3 -B "$H/tieout.py" --self-test
check "test_tieout.py"                   python3 -B "$H/test_tieout.py"
if [ "$fails" -ne 0 ]; then
    echo "install.sh: $fails self-test(s) failed; files are installed in $DEST" >&2
    exit 1
fi
echo "All self-tests passed. Start a new Claude Code session to load the skills and cards."
exit 0

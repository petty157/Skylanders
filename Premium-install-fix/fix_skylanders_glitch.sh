#!/bin/sh

GAME_PKG="com.activision.skylanders.trapteam"
GAME_SUBPATH="files/alchemy.xml"
TARGET_ATTR="minFreeSpaceGameFull"
SCRIPT_DIR="$(cd "$(dirname "$0")" 2>/dev/null && pwd)"
LOCAL_FILE="$SCRIPT_DIR/alchemy.xml"

SEARCH_ROOTS="
/sdcard
/storage/emulated/0
/storage/emulated/1
/storage/self/primary
/mnt/sdcard
/mnt/user/0/primary
/data/media/0
"

if [ -d /storage ]; then
    for d in /storage/*/; do
        case "$d" in
            /storage/emulated/|/storage/self/) continue ;;
        esac
        [ -d "$d" ] && SEARCH_ROOTS="$SEARCH_ROOTS
$d"
    done
fi

patch_file() {
    FILE="$1"

    echo ""
    echo "  Patching: $FILE"

    if [ ! -w "$FILE" ]; then
        echo "  Cannot write to file — permission denied."
        echo "  Grant Termux storage access or run as root."
        return 1
    fi

    if ! grep -qi "$TARGET_ATTR" "$FILE"; then
        echo "  $TARGET_ATTR not found in this file — skipping."
        return 1
    fi

    TARGET_DIR="$(dirname "$FILE")"
    FREE_BYTES=$(df -k "$TARGET_DIR" 2>/dev/null | awk 'NR==2 {print $4 * 1024}')

    if [ -z "$FREE_BYTES" ] || ! echo "$FREE_BYTES" | grep -q '^[0-9]*$' || [ "$FREE_BYTES" -le 0 ]; then
        echo "  Could not read free storage for: $TARGET_DIR"
        return 1
    fi

    FREE_GB=$(awk "BEGIN {printf \"%.2f\", $FREE_BYTES / 1000000000}")
    NEW_VALUE=$(( FREE_BYTES + 1000000000 ))

    echo "  Free storage on this filesystem : $FREE_BYTES bytes (~${FREE_GB} GB)"
    echo "  New $TARGET_ATTR value : $NEW_VALUE bytes"

    sed -i 's/\('"$TARGET_ATTR"'[[:space:]]*=[[:space:]]*"\)[^"]*\(".*\)/\1'"$NEW_VALUE"'\2/I' \
        "$FILE" 2>/dev/null

    if ! grep -q "$NEW_VALUE" "$FILE" 2>/dev/null; then
        sed -i 's/\('"$TARGET_ATTR"'[[:space:]]*=[[:space:]]*"\)[^"]*\(".*\)/\1'"$NEW_VALUE"'\2/' \
            "$FILE"
    fi

    if ! grep -q "$NEW_VALUE" "$FILE"; then
        echo "  Patch failed — value not written."
        return 1
    fi

    echo "  Done. $TARGET_ATTR = \"$NEW_VALUE\""
    return 0
}

echo "Scanning for alchemy.xml across all known storage locations..."

FOUND_FILES=""
FOUND_COUNT=0

for ROOT in $SEARCH_ROOTS; do
    ROOT="${ROOT%/}"
    [ -z "$ROOT" ] && continue
    CANDIDATE="$ROOT/Android/data/$GAME_PKG/$GAME_SUBPATH"
    if [ -f "$CANDIDATE" ]; then
        REAL=$(readlink -f "$CANDIDATE" 2>/dev/null || echo "$CANDIDATE")
        ALREADY=0
        for EXISTING in $FOUND_FILES; do
            EXISTING_REAL=$(readlink -f "$EXISTING" 2>/dev/null || echo "$EXISTING")
            [ "$REAL" = "$EXISTING_REAL" ] && ALREADY=1 && break
        done
        if [ "$ALREADY" -eq 0 ]; then
            FOUND_FILES="$FOUND_FILES $CANDIDATE"
            FOUND_COUNT=$(( FOUND_COUNT + 1 ))
            echo "  Found: $CANDIDATE"
        fi
    fi
done

if [ "$FOUND_COUNT" -eq 0 ]; then
    echo ""
    echo "Game file not found in any known storage location."

    if [ -f "$LOCAL_FILE" ] && grep -qi "$TARGET_ATTR" "$LOCAL_FILE"; then
        echo "Found alchemy.xml in the script directory: $LOCAL_FILE"
        printf "Edit that file instead? [y/N] "
        read ANSWER
        case "$ANSWER" in
            [yY]|[yY][eE][sS])
                patch_file "$LOCAL_FILE"
                STATUS=$?
                ;;
            *)
                echo "Aborted."
                exit 1
                ;;
        esac
    else
        echo "No usable alchemy.xml found. Cannot continue."
        exit 1
    fi

elif [ "$FOUND_COUNT" -eq 1 ]; then
    patch_file "$FOUND_FILES"
    STATUS=$?

else
    echo ""
    echo "WARNING: alchemy.xml found in $FOUND_COUNT locations."
    echo "This can happen with external SD cards, multi-user profiles, or leftover copies."
    echo ""

    i=1
    for F in $FOUND_FILES; do
        echo "  [$i] $F"
        i=$(( i + 1 ))
    done
    echo "  [A] Patch all"
    echo "  [Q] Quit"
    echo ""
    printf "Choice: "
    read CHOICE

    case "$CHOICE" in
        [aA])
            STATUS=0
            for F in $FOUND_FILES; do
                patch_file "$F" || STATUS=1
            done
            ;;
        [qQ]|"")
            echo "Aborted."
            exit 0
            ;;
        *)
            if echo "$CHOICE" | grep -q '^[0-9]*$' && \
               [ "$CHOICE" -ge 1 ] && [ "$CHOICE" -le "$FOUND_COUNT" ]; then
                i=1
                for F in $FOUND_FILES; do
                    if [ "$i" -eq "$CHOICE" ]; then
                        patch_file "$F"
                        STATUS=$?
                        break
                    fi
                    i=$(( i + 1 ))
                done
            else
                echo "Invalid choice. Aborted."
                exit 1
            fi
            ;;
    esac
fi

echo ""
if [ "${STATUS:-0}" -eq 0 ]; then
    echo "All done. Re-run this script if your free storage increases by more than 1 GB."
else
    echo "One or more files could not be patched. See messages above."
    exit 1
fi

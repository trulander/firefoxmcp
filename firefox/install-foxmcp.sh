#!/bin/bash
set -e

MOZ_DIR="/root/.mozilla/firefox"
mkdir -p "$MOZ_DIR"

PROFILE_NAME="default-esr"
PROFILE_DIR="$MOZ_DIR/$PROFILE_NAME"

if [ ! -d "$PROFILE_DIR" ]; then
    echo "Creating manual Firefox profile at $PROFILE_DIR"
    mkdir -p "$PROFILE_DIR"
    
    cat <<EOF > "$MOZ_DIR/profiles.ini"
[General]
StartWithLastProfile=1

[Profile0]
Name=default
IsRelative=1
Path=$PROFILE_NAME
Default=1
EOF
fi

EXT_DIR="$PROFILE_DIR/extensions"
mkdir -p "$EXT_DIR"
cp /opt/foxmcp.xpi "$EXT_DIR/foxmcp@codemud.org.xpi"
echo "FoxMCP extension copied to $EXT_DIR"

# Configure the extension to be enabled by default
# This often requires adding prefs.js
if [ ! -f "$PROFILE_DIR/prefs.js" ]; then
    echo 'user_pref("extensions.enabledScopes", 15);' > "$PROFILE_DIR/prefs.js"
    echo 'user_pref("extensions.autoDisableScopes", 0);' >> "$PROFILE_DIR/prefs.js"
fi

echo "FoxMCP setup complete"

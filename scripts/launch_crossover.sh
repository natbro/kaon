#!/bin/sh
set -x

# edit this if you have multiple varients of CrossOver installed, such as CrossOver-25beta.app
crossover="/Applications/CrossOver.app"
bottle="$1"

export DISPLAY=:`defaults read com.codeweavers.CrossOver Display`
export DYLD_FALLBACK_LIBRARY_PATH="$crossover/Contents/SharedSupport/X11/lib:$HOME/lib:/lib:/usr/lib:/usr/X11/lib"
export FONT_ENCODINGS_DIRECTORY="$crossover/Contents/SharedSupport/X11/lib/X11/fonts/encodings/encodings.dir"
export FONTCONFIG_PATH="$crossover/Contents/SharedSupport/X11/etc/fonts"
export FONTCONFIG_ROOT="$crossover/Contents/SharedSupport/X11"
export VERSIONER_PERL_PREFER_32_BIT=yes
export CX_BOTTLE="$bottle"
export PATH="$crossover/Contents/SharedSupport/CrossOver/bin:$PATH"

# This picks up the wine binary from newly modified PATH, first removing the passed in bottle from $1 used above
shift
wine "$@"

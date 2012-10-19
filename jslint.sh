#!/bin/bash

INSTALL=<<INSTALLTEXT
spidermonkey js interpreter not installed.
On Mac OS:
    brew install spidermonkey

On Ubuntu:
    sudo apt-get install spidermonkey-bin (in launchpad)
    or:
    sudo apt-get install rhino
INSTALLTEXT
# Spidermonkey -- first test for js availability
WHICH_JS=`which js`
if [ "$WHICH_JS" = '' ]; then
    echo $INSTALL
    exit 1
fi


JSFILES="static/js/*.js"

TO_PROCESS=""
if [ $# -ne 0 ]; then
    for file in $*; do
        for f in $JSFILES; do
            if [ $f == $file ]; then
                TO_PROCESS="$TO_PROCESS $f"
            fi
        done
    done
else
    TO_PROCESS=$JSFILES
fi

ERRORS=""
for f in $TO_PROCESS; do
    output=`js -f jslint.js < $f`
    if [ "$output" != "jslint: No problems found." ]; then
        ERRORS="$ERRORS$f:\n$output\n\n"
    fi
done

if [ "$ERRORS" != "" ]; then
    echo -ne "====================jslint errors====================\n$ERRORS"
    exit 1
else
    echo "jslint success"
    exit 0
fi

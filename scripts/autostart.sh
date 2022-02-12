#!/bin/sh

killall -q touchpad-indicator
touchpad-indicator &
wal -R

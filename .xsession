#!/bin/sh
#
# Custom xsession script for x session init.

#=============ARK========================================================
# Setup compose key and F13-F24 keys
#xkbcomp -w0 -I$HOME/.config/xkb $HOME/.config/xkb/mymap.xkb $DISPLAY
#
# The problem with this implementation is that any udev rule trigger will
# reset the default keyboard layout. Should be implemented directly in
# /etc/X11/xorg.conf.d/00-keyboard.conf, or rather in the
# jeany_setup/keyboard_setup.sh script as a localectl option
#========================================================================

# Run xbindkeys for ~/.xbindkeysrc
xbindkeys

# Setup screens, config for 2 x 16:9 horizontal FHD monitors
xrandr --output HDMI-1 --primary --left-of HDMI-0

# Enable mouse natural scrolling (udev rule also set, but this is needed
# for the initial setup):
. ~/bin/jeany_scripts/mouse_wheel_invert/mouse_wheel_invert.sh

# Wacom Intuos initial setup:
. ~/bin/jeany_scripts/wacom/wacom_config.sh

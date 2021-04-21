#!/bin/bash

# Written by Jean Yves Beaucamp - 2021
#
# INSTRUCTIONS:
# Run with a xbindkeys binding to one of the Pad's buttons, or as a standalone script.
#
# Options:
#   --manual-config=<NUM> : manual setting to display <NUM> from the $MONITORS array below.


# ================================================================================
# CONFIGURATION

# Set this to your generic device name. Find it by running:
#
# xsetwacom --list devices
#
# There will be multiple entries listed for the same device. For example: 
#   > xsetwacom --list devices
#   Wacom Intuos PT S 2 Pen stylus  	id: 8	type: STYLUS
#   Wacom Intuos PT S 2 Finger touch	id: 9	type: TOUCH
#   Wacom Intuos PT S 2 Pad pad     	id: 10	type: PAD
#
# In this case, you should set: DEVICE='Wacom Intuos PT S 2'
device='Wacom Intuos PT S 2'

# These numbers are specific for each "stylus" device. Get them by running:
# 
# xsetwacom --set $DEVICE_STYLUS ResetArea
# xsetwacom --get $DEVICE_STYLUS Area
#
# with DEVICE_STYLUS="Wacom Intuos PT S 2 Pen stylus"
area_x=15200
area_y=9500

# Set monitors:
# You can see a list of all connected monitors by running
#
# xrandr -q --current | sed -n 's/^\([^ ]\+\) connected .*/\1/p'
#
# Complete the following array with the monitors you want to include in the switcher. The 'desktop' entry corresponds to the entire desktop setup.
# WARNING: If using the NVidia binary drivers then if 'HDMI-0', 'HDMI-1', ... don't work, use instead the pairs 'HDMI-0@HEAD-0', 'HDMI-1@HEAD-1', ... according to the monitor number and input type.
monitors=( 'desktop' 'HDMI-1@HEAD-0' 'HDMI-0@HEAD-1' )
#
# Temporary state file:
ms_state_file='/tmp/wacom_monitor_switcher.dat'

# ================================================================================

# Get IDs for all asociated devices:
id_stylus=$(xsetwacom --list | grep -i "$device" | grep -i "stylus" | awk '{print $(NF-2)}')
#id_touch=$(xsetwacom --list | grep -i "$device" | grep -i "touch" | awk '{print $(NF-2)}')
#id_pad=$(xsetwacom --list | grep -i "$device" | grep -i "pad" | awk '{print $(NF-2)}')

#----------------------------------------------------------------------------------

#MONITOR SWITCHER:

# Check for temp state file. If not available or value is corrupted, initialilze to ms_state=0 (First value); otherwise increment by 1 and round-robin:

# If there is no file, initialize to 0
if [[ ! -z $1 ]] && [[ $1 == '--manual-config='* ]]; then
    ms_state=${1#*'='}
    num_regex='^[0-9]+$'
    if [[ ! $ms_state =~ $num_regex ]] || [ $ms_state -lt 0 -o $ms_state -ge "${#monitors[@]}" ]; then
        ms_state=0
    fi
elif [ ! -f "$ms_state_file" ]; then
    ms_state=0
else
    ms_state=$(cat "$ms_state_file")
    
    # Check if file contents are numbers (always >= 0, as the regex doesn't contain signs), otherwise reset to ms_state=0
    num_regex='^[0-9]+$'
    if [[ ! $ms_state =~ $num_regex ]]; then
        ms_state=0
    fi

    # Increment by 1
    ms_state=$((ms_state + 1))

    # Round-Robin
    if [ $ms_state -ge "${#monitors[@]}" ]; then
        ms_state=0
    fi
fi

# Save file with new state:
echo "$ms_state" > $ms_state_file

# Get screen resolutions by polling to xrandr
ms_state_name="${monitors[$ms_state]}"
if [ "$ms_state_name" = "desktop" ]; then
    line=$(xrandr -q --current | sed -n 's/^Screen 0:.*, current \([0-9]\+\) x \([0-9]\+\),.*/\1 \2/p')
else
    if [[ $ms_state_name == *'@'* ]]; then
        line=$(xrandr -q --current | sed -n "s/^${ms_state_name%'@'*}"' connected\( primary\)\? \([0-9]\+\)x\([0-9]\+\)+.*/\2 \3/p')
        ms_state_name="${ms_state_name#*'@'}"
    else
        line=$(xrandr -q --current | sed -n "s/^${ms_state_name}"' connected\( primary\)\? \([0-9]\+\)x\([0-9]\+\)+.*/\2 \3/p')
    fi
fi

read monitor_width monitor_height <<< "$line"
if [ -z "$monitor_width" -o -z "$monitor_height" ]; then
    echo 'xrandr could not find the specified monitor resolution. Aborting...'
    exit 1
fi

# New values respect aspect ratio:
ratio_area_y=$(( area_x * monitor_height / monitor_width ))
ratio_area_x=$(( area_y * monitor_width / monitor_height ))

if [ "$area_y" -gt "$ratio_area_y" ]; then
	new_area_x="$area_x"
	new_area_y="$ratio_area_y"
else
	new_area_x="$ratio_area_x"
	new_area_y="$area_y"
fi

if [ -z "$(xsetwacom --list devices)" ]; then
    echo 'xsetwacom had no devices connected'
    exit 1
else
	xsetwacom --set "$id_stylus" Area 0 0 "$new_area_x" "$new_area_y"
	xsetwacom --set "$id_stylus" MapToOutput "$ms_state_name"
fi


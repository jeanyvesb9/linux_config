#!/bin/bash

# Replace DEVICE with proper mouse name after running:
# xinput list
device='Logitech G502 HERO Gaming Mouse'

# Replace PROPERTY_NAME with corresponding name after running
# xinput list-props $DEVICE
property_name='libinput Natural Scrolling Enabled'

#Check for a running X11 session in order to avoid errors in udev trigger before XOrg loads
if ! timeout 1s xset q &>/dev/null; then
    exit 1
fi

# Wait for up to 5 seconds for the device to show up
counter=0
while [ -z "$(xinput list | grep -i "${device}")" ]; do
    if [ $counter -eq 11 ]; then
        echo "No $device connected."
        exit 1
    fi
    sleep .5 #Wait 0.5 seccond
    counter=$((counter + 1))
done

xinput set-prop "$device" "$property_name" 1


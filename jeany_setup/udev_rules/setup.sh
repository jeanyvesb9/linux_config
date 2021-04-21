#!/bin/bash
#
# Copyright (C) 2021 Jean Yves Beaucamp <jeanyvesb9@gmail.com>
#
# Copy udev rules for custom scripts that involve hardware interactions to the
# default location

if [ "$EUID" -ne 0 ]; then
  echo 'Please run as root'
  exit 1
fi

cp ./*.rules /etc/udev/rules.d/

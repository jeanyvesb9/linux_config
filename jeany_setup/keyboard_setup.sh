#!/bin/sh
#
# Copyright (C) 2021 Jean Yves Beaucamp <jeanyvesb9@gmail.com>
#
# Setup keyboard with the following parameters:
#   -Layout: us
#   -Model: pc104
#   -Variant: , (no-variant)
#   -Options: compose:menu

localectl set-x11-keymap us pc104 , "compose:ralt, compose:menu"

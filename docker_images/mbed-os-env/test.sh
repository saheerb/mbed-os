#!/bin/sh
set -x
MBED_OS_VERSION=$1
# if master; then
# EXAMPL_VERSION="development"
# else
# # if tagged if tag is available us it
# # if tag is not available? use development
# fi

mbed import mbed-os-example-blinky
cd mbed-os-example-blinky
git checkout ${MBED_OS_VERSION}
mbed deploy 
# symlink
mbed compile -m K64F -t GCC_ARM
mbed-tools compile -m K64F -t GCC_ARM

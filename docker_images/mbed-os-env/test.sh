#!/bin/sh
set -x
MBED_OS_VERSION=$1
exit 1
if [ ${MBED_OS_VERSION} = "master" ];then
    EXAMPLE_VERSION="development"
else
    EXAMPLE_VERSION=${MBED_OS_VERSION}
fi

mbed import mbed-os-example-blinky
cd mbed-os-example-blinky
git checkout ${EXAMPLE_VERSION}
mbed deploy 
mbed compile -m K64F -t GCC_ARM
mbed-tools compile -m K64F -t GCC_ARM


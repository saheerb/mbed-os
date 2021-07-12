#!/bin/sh
set -x
IMAGE_RELEASE_TYPE=$1
MBED_OS_VERSION=$2

# 
mbed import mbed-os-example-blinky
cd mbed-os-example-blinky

# when development images or PR checks are getting tested, use "development" version of example application
# development versions and PR should only happen to master branch, if it is happening to other branch extend the if conditions
if [ ${IMAGE_RELEASE_TYPE} == "DEVELOPMENT" ] || [ ${IMAGE_RELEASE_TYPE} == "PR" ];then
    if [ ${MBED_OS_VERSION} == "master" ];then
        EXAMPLE_VERSION="development"
    else
        echo "Not implemented"
        exit 1
    fi
# When mbed-os tag is applied, and workflow is triggered to build RELEASE image, example application with same tag will be available yet.
# use release candidate branch to test the image in that case.
# When RELEASE image is passively checked, tag should be available in example application repo, then use it.
elif [ ${IMAGE_RELEASE_TYPE} == "RELEASE" ] ; then
    if git rev-parse "$MBED_OS_VERSION" >/dev/null 2>&1; then
        EXAMPLE_VERSION=$MBED_OS_VERSION
    else
        EXAMPLE_VERSION="release_candidate"
    fi
fi


echo ${EXAMPLE_VERSION}
git checkout ${EXAMPLE_VERSION}

# regardless of example version, use the version of mbed-os getting built in the workflow.
rm -rf mbed-os
ln -s ../mbed-os mbed-os

# build using CLI1
mbed compile -m K64F -t GCC_ARM

# build using CLI2
mbed-tools compile -m K64F -t GCC_ARM                                                                                                                                                                                                                                                    

# mbed-os-env docker management

# Table of contents

1. [WARNING: THIS IS AN EXAMPLE DESIGN DOCUMENT](#warning-this-is-an-example-design-document).
1. [Standardized error coding and error handling](#standardized-error-coding-and-error-handling).
1. [Table of contents](#table-of-contents).
        1. [Revision history](#revision-history).
1. [Introduction](#introduction).
        1. [Overview and background](#overview-and-background).
        1. [Requirements and assumptions](#requirements-and-assumptions).
1. [System architecture and high-level design](#system-architecture-and-high-level-design).
        1. [System architecture and component interaction](#system-architecture-and-component-interaction).
1. [Detailed design](#detailed-design).
1. [Usage scenarios and examples](#usage-scenarios-and-examples).
1. [Tools and configuration changes](#tools-and-configuration-changes).
1. [Other information](#other-information).
        1. [Reusability](#reusability).
        1. [Deprecations](#deprecations).
        1. [References](#references).

### Revision history

1.0 - Initial version - Saheer Babu - 22/6/2021

# Introduction

### Overview and background

docker image mbed-os-env bundles all the necessary tools to provide a minial environment to build and test mbed-os applications. This docker image shall be used in Continuous Integration pipelines where mbed-os tools and dependancies are required. This document explains use cases, versioning strategy of the docker image and github action workflows that creates these docker images.

### Goals

* Distribution of docker image that is compatible with released version of mbed-os. 
* Providing docker image that is compatible with HEAD of "main" branch. 
* Keeping the released and development docker image up to date.


### types of docker images

* Production docker image
These are docker images compatible with a released version of mbed-os. For example when `mbed-os-6.14.0` is released, a docker image with tag `mbed-os-6.14-latest` is available.

* Development docker image
These are docker images compatible with a `HEAD` of the mbed-os branch. For example when main-latest docker image is available which is comptible with `HEAD` of `main` branch.


### Type of docker image updates

There are two type of docker image updates. 

**Active Updates** 
Typically these type of changes that involve modifications in Dockerfile or changes in the requirements.txt. Examples: mbed-os adds support for new compiler version and hence needs Dockerfile update.

**Passive updates** 
These are scheduled updates on existing mbed-os-env images to provide security and bug fixes of dependent packages. In updates like this, there will be no change in Dockerfile but rebuilding the Dockerfile provides a new docker image with updated tools and packages. 

### Type of docker tags

For the purpose of mbed-os-env docker management we will need to apply a few docker tags on the image. 

**latest tags**
These tags have the format `<name>-latest`, for example `mbed-os-6-latest`. The `-latest` at the end indicates that the same tag may be reapplied to another image, when a docker image is updated. This obviously means, a user pulling the image with same tag name may get different images at different point of time. 

**fixed tags**
using latest tags, user can retrieve an updated version of docker image. Trubleshooting could become tricky if docker images are updated and new images are retrieved in the middle of troubleshooting session. Also, some user could decide not to get updated version and would want to stick to a fixed version.

For reasons stated above, all the docker images are also applied a fixed tag. These tags are only applied to one image and never reused. Tags are of the format `mbed-os-<version>-<date>`, example `mbed-os-6.14.0-2021.06.19T04.43.51`, `main-2021.06.19T04.43.51` etc

### Dockerfile versioning
mbed-os-env image is created with dockerfile stored in this repository itself. This provides easy versioning of Dockerfile as it will follows the same versioning strategy of mbed-os. 

### Docker image versioning

## docker image tag creation and updates example

The picture below illustrates a typical situation where mbed-os accepts changes to main branch on daily basis and makes releases on regular basis.

**On Day-X** There are some changes for active updates (ie, dockerfile has been changed), so these are the docker images created or updated

* main-latest 
* main-day-x - This is a fixed tag

 :+1: At night, main-latest tag is checked for Passive Update. 

**On Day-X+1** Though there are commits to mbed-os source repository. These do not involve changes to Dockerfiles or dependencies like requirements.txt. Hence, no docker image is created at the time of merging the commit. At night, main-latest tag is checked for Passive Update.

**On Day-X+2** A new release `mbed-os-6.14.0` is created. This creates an image with following docker tag.

* mbed-os-6-latest - This docker tag could be used to get a compaitble image for latest mbed-os-6 release.
* mbed-os-6.14-latest - This docker tag  could be used to work with updated mbed-os-6.14 release. This image is passively updated till next mbed-os release on the branch (typically till mbed-os-6.15.0)
* mbed-os-6.14-day-x - A fixed docker tag 

:+1: mbed-os-6.14-latest, and mbed-os-6-latest will be passively updated everynight from now on.

**On Day X+10** Another new release mbed-os-6.15.0 is made. This creates an image with following docker tag.

* mbed-os-6-latest
* mbed-os-6.15-latest
* mbed-os-6.15-day-x

From this point, mbed-os-6.14-latest will no longer be passively updated. From this point, only mbed-os-6.15-latest is selected for passive update. Only last release version is passively updated on a branch. 

## Workflows

There are 3 main workflows

* PR check
The purpose of this workflow is to make sure build, and test of mbed-os-env docker image works as expected. Hence this workflow is triggered when mbed-os PR is created with changes in Dockerfile, test files, or workflow files itself has some modifications. Since most of the mbed-os PR doesn't contain docker image related changes, this workflow is not expected to be triggered often.

* Development Docker image publish
The purpose of this workflow is to update development docker image either when there is an active update or at nightly for passive update.

This workflow can also be triggered manually to update the development image (during the day if needed for example)

* Production Docker image Creation/Update
This workflow will create a new docker image with versioning strategy describe above. Also, triggered nightly for passive update.

This workflow can also be triggered manually to update an old version of released docker image. For example, this workflow could be manually tiggered to update mbed-os-6.14-latest after mbed-os-6.15.0 is released



## Pipeline

docker image management follows typically CI pipeline of build, test, relese follows.

There are some details worth mentioning though.

**Build**

docker buildx command is used for creating multi architecture docker image. To build this with method, one needs to push the image to a remote repository while building it. Since, we need to "test" before release. These are pushed to a temporary docker repository just after building.

github container registry doesn't implement yet all the docker manifest APIs. Hence, a few features like deleting tag from an image is not available yet. For implementing the workflows, we create 

**Test**
test.sh script takes care of all the testing.

**Release**
release means moving the image from temporary repository to production repository with necessary tags.

docker image in temporary area is also pruned by checking number of dates since updated.


## Docker repository
github provides free docker image storage for public repositories in github packages. The workflows make use of {{ secrets.GITHUB_TOKEN }}  https://docs.github.com/en/actions/reference/authentication-in-a-workflow 

The packages are directly visible in mbed-os repository.

For deleting images from temporary repository, a new token GITHUB_DELETE_IMAGE_TOKEN needs to be added with package delete perimissions.

## Workflow for forks

As there is a scheduled trigger of workflow development and release workflow is enabled only when "ARMMbed" repository owner criteria is met. For development, one can change this, make necessary development and put this back to "ARMMbed" when creating pull request to "ARMMbed/mbed-os".

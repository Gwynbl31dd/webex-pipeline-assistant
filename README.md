# pipeline_assistant

[![CI](https://github.com/Gwynbl31dd//webex-pipeline-assistant/actions/workflows/docker-image.yml/badge.svg)](https://github.com/Gwynbl31dd//webex-pipeline-assistant/actions/workflows/docker-image.yml)

This project is a docker image that can publish any test results to Cisco Webex. (Basically, zip a folder an push it to a list of Webex rooms)

The only requirement is populating the environment variable and having a webex token available. (Easy... I know...)

I recommend creating a bot and using it's token [Webex-Bot](https://developer.webex.com/docs/bots)

## Build the docker image

You can download the image directly from [docker-hub](https://hub.docker.com/r/gwynbl31dd/webex-pipeline-assistant)

Or build it yourself using :

```bash
make image
```

There is also a ``docker-compose.yml`` file you can use as an example. 

### Use the image

You can run it with a single command. I tried to make it as simple as possible for an easy integration with any pipeline (gitlab, concourse, github,...)

```bash
docker run -e "WEBEX_TEAMS_ACCESS_TOKEN=$WEBEX_TEAMS_ACCESS_TOKEN" -e "WEBEX_ROOMS=[\"Room name\"]" -e "WEBEX_PEOPLE=[\"your@mail.com\"]" -e "RESULT_PATH=/results" -v ${PWD}/results:/results gwynbl31dd/webex-pipeline-assistant:latest
```

You can add as many people and room you need. (Avoid spamming though :O ) 

## Environment variables

### Required

* WEBEX_TEAMS_ACCESS_TOKEN: This is your token (Preferably a bot, but you can use a personal access token if you which)
* WEBEX_ROOMS: List of rooms where you will publish the results. Example: ``["Room1","Room2",...]``
* WEBEX_PEOPLE: List of people you want to add to these rooms, you need to use their email address. Example: ``["email@1.com","email@2.com",...]``
* RESULT_PATH: The path were you want to grab the results. (Or where you mounted them if using docker) Example: ``/tmp/results``

### Optional

* WEBEX_HTTPS_PROXY: If you use a proxy, that's where you put it. Example ``http:myproxy.local:8080``
* WEBEX_HTTP_PROXY: If you use a proxy (in http), that's where you put it. Example ``http:myproxy.local:8080``

## Example

### Gitlab

If you use gitlab, here is an example I use for one of my own service:

* I build something (It does not matter what, here it's a vlan package for NSO)
* I run my test using something. (Here I use robotframework in a container, and save the results in ``./results`` )
* I run the webex-pipeline-assistant and mount the ``results`` to a result folder ``{PWD}/results:/results``
* That's it. Your result are going to be zipped and pushed to your rooms. 

```yaml
image: creatiwww/docker-compose:latest

variables:
  PACKAGE_REGISTRY_URL: "${CI_API_V4_URL}/projects/${CI_PROJECT_ID}/packages/generic"
  PACKAGE_NAME: "vlan"

services:
  - docker:dind

stages:
  - build
  - release

build:
  stage: build
  script:
    - docker login -u gitlab-ci-token -p $CI_BUILD_TOKEN $CI_REGISTRY_IMAGE
    - echo "IMAGE_APP_TAG=$STAGE_IMAGE_APP_TAG" >> .env
    - chmod +x nso/pre-start/*
    - chmod +x nso/post-start/*
    - docker-compose run tests
    - docker run -e "WEBEX_TEAMS_ACCESS_TOKEN=${WEBEX_TOKEN}" -e "WEBEX_ROOMS=[\"NSO Service pipeline\"]" -e "WEBEX_PEOPLE=[\"apaulin@cisco.com\"]" -e "RESULT_PATH=/results" -v ${PWD}/results:/results gwynbl31dd/webex-pipeline-assistant:master
    - cd nso/packages && for dir in `ls`; do tar -cvzf ${dir}.tar.gz ${dir}; done
  only:
    - master
  artifacts:
    paths:
      - nso/packages/
      - results
```

### Github

if you use github, it is pretty much similar. You just need to build the container and mount the volume.

```yaml
name: Docker Image CI

on:
  push:
    branches: [ "develop" ]
  pull_request:
    branches: [ "develop" ]

jobs:

  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Run the Docker image
      run: docker run -e "WEBEX_TEAMS_ACCESS_TOKEN=${{ secrets.WEBEX_TOKEN }}" -e "WEBEX_ROOMS=[\"Webex-assistant-pipeline\"]" -e "WEBEX_PEOPLE=[\"apaulin@cisco.com\"]" -e "RESULT_PATH=/results" -v ${PWD}:/results gwynbl31dd/webex-pipeline-assistant:latest
```

## Development

Read the [CONTRIBUTING.md](CONTRIBUTING.md) file.

## Maintainer

* Anthony Paulin <paulin.anthony@gmail.com>
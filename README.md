---
# pipeline_assistant

[![CI](https://github.com/Gwynbl31dd//webex-pipeline-assistant/actions/workflows/docker-image.yml/badge.svg)](https://github.com/Gwynbl31dd//webex-pipeline-assistant/actions/workflows/docker-image.yml)

This project is a docker image that can publish any test results to Cisco Webex. (Basically, zip a folder an push it to a list of Webex rooms)

The only requirement is populating the environment variable and having a webex token available. (Easy... I know...)

## Build the docker image

You can download the image directly from [docker-hub](https://hub.docker.com/r/gwynbl31dd/webex-pipeline-assistant)

Or build it using 

```bash
make image
```

There is also a ``docker-compose.yml`` file you can use as an example.

### Use the image

You can run it with a single command. I tried to make it as simple as possible for an easy integration with gitlab, concourse or github actions.

```bash
docker run -e "WEBEX_TEAMS_ACCESS_TOKEN=$WEBEX_TEAMS_ACCESS_TOKEN" -e "WEBEX_ROOMS=[\"Room name\"]" -e "WEBEX_PEOPLE=[\"your@mail.com\"]" -e "RESULT_PATH=/results" -v /tmp/results:/results gwynbl31dd/webex-pipeline-assistant:master
```

You can add as many people and room you need. (Avoid spamming though) 

## Development

Read the [CONTRIBUTING.md](CONTRIBUTING.md) file.

## Maintainer

* Anthony Paulin <paulin.anthony@gmail.com>

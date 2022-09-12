---
# pipeline_assistant

[![codecov](https://codecov.io/gh/Gwynbl31dd/pipeline_assistant/branch/main/graph/badge.svg?token=pipeline_assistant_token_here)](https://codecov.io/gh/apaulin/pipeline_assistant)
[![CI](https://github.com/Gwynbl31dd/pipeline_assistant/actions/workflows/main.yml/badge.svg)](https://github.com/apaulin/pipeline_assistant/actions/workflows/main.yml)

This project is used to create a docker image that can publish the test results to Cisco Webex. 

The only requirement is populating the environment variable and having a webex token available.

## Build the docker image

You can download the image directly from [docker-hub]()

Or build it using 

```bash
make image
```

There is also a ``docker-compose.yml`` file you can use as an example.

## Install it from PyPI

```bash
pip install pipeline_assistant
```

## Usage

We recommand using a virtual environment to isolate the project from the system:

```bash
apt install python3.10-venv
```

```bash
$ make virtualenv
$ source .venv/bin/activate
$ make install
$ pipeline_assistant
```

## Structure

Lets take a look at the structure of this template:

```text
├── Dockerfile               # The file to build a container using docker
├── CONTRIBUTING.md          # Onboarding instructions for new contributors
├── docs                     # Documentation site (add more .md files here)
│   └── index.md             # The index page for the docs site
├── .github                  # Github metadata for repository
├── .gitignore               # A list of files to ignore when pushing to Github
├── HISTORY.md               # Auto generated list of changes to the project
├── LICENSE                  # The license for the project
├── Makefile                 # A collection of utilities to manage the project
├── MANIFEST.in              # A list of files to include in a package
├── mkdocs.yml               # Configuration for documentation site
├── project_test             # The main python package for the project
│   ├── dna_center.py        # The base module for the project
│   ├── __init__.py          # This tells Python that this is a package
│   ├── __main__.py          # The entry point for the project
│   ├── dnac_requester.py    # small helper module to make requests to DNA Center
│   └── VERSION              # The version for the project is kept in a static file
├── README.md                # The main readme for the project
├── setup.py                 # The setup.py file for installing and packaging the project
├── requirements.txt         # An empty file to hold the requirements for the project
├── requirements-test.txt    # List of requirements for testing and devlopment
├── setup.py                 # The setup.py file for installing and packaging the project
└── tests                    # Unit tests for the project (add more tests files here)
    ├── conftest.py          # Configuration, hooks and fixtures for pytest
    ├── __init__.py          # This tells Python that this is a test package
    └── test_base.py         # The base test case for the project
```

## The Makefile

All the utilities for the template and project are on the Makefile

```bash
❯ make
Usage: make <target>

Targets:
help:             ## Show the help.
install:          ## Install the project in dev mode.
fmt:              ## Format code using black & isort.
lint:             ## Run pep8, black, mypy linters.
test: lint        ## Run tests and generate coverage report.
watch:            ## Run tests on every change.
clean:            ## Clean unused files.
virtualenv:       ## Create a virtual environment.
release:          ## Create a new tag for release.
docs:             ## Build the documentation.
switch-to-poetry: ## Switch to poetry package manager.
init:             ## Initialize the project based on an application template.
```

## Development

Read the [CONTRIBUTING.md](CONTRIBUTING.md) file.

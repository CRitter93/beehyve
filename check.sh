#!/bin/bash
isort -q -c --profile black .
black --check -q -l 120 .
flake8 -q .
mypy beehyve
bandit -q -c bandit.yml -r beehyve
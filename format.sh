#!/bin/bash
isort --profile black .
autoflake -r --in-place --remove-unused-variables .
black -l 120 .

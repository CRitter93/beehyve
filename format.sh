#!/bin/bash
isort .
autoflake -r --in-place --remove-unused-variables .
black .

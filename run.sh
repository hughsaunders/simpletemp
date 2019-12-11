#!/bin/bash -xeu

. venv/bin/activate

FLASK_APP=temp.py flask run \
	-h 0.0.0.0 \
	-p 8080

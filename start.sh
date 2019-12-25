#! /bin/bash
export FLASK_APP=src/main.py
export FLASK_DEBUG=1
flask resetdb
flask run --host=0.0.0.0 --port=5000

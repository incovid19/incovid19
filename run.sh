#!/bin/sh
cp -a ./. /data/incovid19/
jupyter lab --allow-root --ip 0.0.0.0 --ServerApp.token=$NOTEBOOK_PASS
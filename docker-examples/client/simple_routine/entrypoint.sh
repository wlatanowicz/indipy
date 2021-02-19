#!/usr/bin/env bash

wait-for-dep tcp://$INDISERVER_HOST:$INDISERVER_PORT

python $@

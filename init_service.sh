#!/bin/sh
/docker-entrypoint.sh echo ""
/usr/bin/supervisord -t -n

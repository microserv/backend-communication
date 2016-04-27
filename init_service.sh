#!/bin/sh
/docker-entrypoint.sh echo ""
su - root
/usr/bin/supervisord -t -n

#!/bin/sh
/docker-entrypoint.sh
su - root
/usr/bin/supervisord -t -n

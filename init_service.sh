#!/bin/sh
/usr/local/bin/docker-entrypoint.sh
su - root
/usr/bin/supervisord -t -n

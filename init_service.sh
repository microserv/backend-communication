#!/bin/sh
/usr/local/bin/docker-entrypoint.sh
su - root
/user/bin/supervisord -t -n

#!/bin/sh
/docker-entrypoint.sh
su - root
/user/bin/supervisord -t -n

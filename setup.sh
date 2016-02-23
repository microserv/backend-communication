#!/bin/bash

set -e
echo "This script assumes that you are using debian or ubuntu."
echo -e "The following packages will be installed: libzmq3\n"

sudo aptitude install libzmq3

echo "All done!"

#!/bin/bash

set -e
echo "This script assumes that you are using debian or ubuntu."
echo -e "The following packages will be installed: libzmq3\n"

sudo apt-get install libzmq3 libzmq3-dev

echo "All done!"

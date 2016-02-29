#!/bin/bash
pip install virtualenv
virtualenv venv && source venv/bin/activate
pip install -r requirements.txt
git clone https://github.com/microserv/entangled-dht entangled && cd entangled
python setup.py install
cd ..
rm -rf entangled

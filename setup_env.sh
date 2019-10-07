#!/bin/bash

if [ -d .ve/ ]; then
    echo "$0: Found existing .ve/"
    exit 1
fi

virtualenv -p python3 .ve/
source .ve/bin/activate
pip install -r requirements.txt

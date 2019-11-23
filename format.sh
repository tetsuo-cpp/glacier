#!/bin/bash

if [ ! -d .ve/ ]; then
    echo "$0: No .ve/ found. Running setup_env..."
    bash setup_env.sh
fi

source .ve/bin/activate
black --line-length=100 glacierc
black --line-length=100 glacier/
black --line-length=100 tests/

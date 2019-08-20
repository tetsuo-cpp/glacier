#!/bin/bash

if [ ! -d .ve/ ]; then
    echo "$0: No .ve/ found. Running setup_env..."
    bash setup_env.sh
fi

if [ "$#" -ne 1 ]; then
    echo "$0: Usage ./system_test.sh [TEST_NAME]"
    exit 1
fi

test_name=$1
source .ve/bin/activate
python glacierc.py \
       "system_tests/${test_name}/${test_name}.glc" \
       "system_tests/${test_name}/${test_name}.bc"
./glaciervm "system_tests/${test_name}/${test_name}.bc"

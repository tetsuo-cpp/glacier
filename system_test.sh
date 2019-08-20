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
test_prefix="system_tests/${test_name}/${test_name}"
source_path="${test_prefix}.glc"
bytecode_path="${test_prefix}.bc"

source .ve/bin/activate

python glacierc.py "${source_path}" "${bytecode_path}" || exit 1

./glaciervm "${bytecode_path}" || exit 1

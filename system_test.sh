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
echo "0: Running test $test_name"

python glacierc.py "$source_path" "$bytecode_path" || exit 1

output_path=$(mktemp)
expected_path="${test_prefix}.out"
./glaciervm "$bytecode_path" > "$output_path" || exit 1
cmp "$output_path" "$expected_path"
if [ $? -ne 0 ]; then
    echo "$0: Does not match expected output"
    echo "$0: Failed test $test_name"
    exit 1
fi
rm "$output_path"
echo "$0: Passed test $test_name"
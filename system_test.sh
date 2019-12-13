#!/bin/bash

function cleanup {
    echo "$0: Cleaning up $output_path"
    rm "$output_path"
}

trap cleanup EXIT

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
echo "$0: Running test $test_name"
if [[ "$test_prefix" == *_error ]]; then
    output_path=$(mktemp)
    expected_path="${test_prefix}.err"
    ./glacierc "$source_path" -o "$bytecode_path" > "$output_path" && exit 1
    cmp "$output_path" "$expected_path"
    if [ $? -ne 0 ]; then
        echo "$0: Does not match expected error output"
        exit 1
    fi
    echo "$0: Passed test $test_name"
    exit 0
else
    ./glacierc "$source_path" -o "$bytecode_path" || exit 1
fi

output_path=$(mktemp)
expected_path="${test_prefix}.out"
./glaciervm "$bytecode_path" > "$output_path" || exit 1
cmp "$output_path" "$expected_path"
if [ $? -ne 0 ]; then
    echo "$0: Does not match expected output"
    echo "=== Expected ==="
    cat "$expected_path"
    echo "=== Actual ==="
    cat "$output_path"
    echo "$0: Failed test $test_name"
    exit 1
fi
echo "$0: Passed test $test_name"

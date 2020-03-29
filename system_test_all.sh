#!/bin/bash

tests=$(ls system_tests/)

for t in $tests; do
    bash system_test.sh $t || exit 1
done

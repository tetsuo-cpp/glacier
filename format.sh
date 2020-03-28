#!/bin/bash

if [ ! -d .ve/ ]; then
    echo "$0: No .ve/ found. Running setup_env..."
    bash setup_env.sh
fi

# Format Python files with Black.
source .ve/bin/activate
black --line-length=100 glacierc
black --line-length=100 glacierd
black --line-length=100 compiler/
black --line-length=100 tests/

# Format C files with Clang Format.
git ls-files | grep "\.\(c\|h\)$" | xargs clang-format -i

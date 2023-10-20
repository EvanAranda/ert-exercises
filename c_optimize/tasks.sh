#!/bin/bash
set -e

compile() {
    gcc -o $1 \
        -lm \
        -Wall \
        $1.c
}

profile() {
    compile $1
    /usr/bin/time -l -o time_"$1".txt "./$1"
}

"$@"

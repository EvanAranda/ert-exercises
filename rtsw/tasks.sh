#!/bin/bash
set -e

ENV="${ENV:-dev}"
VENV_DIR=.venv

_log() {
    time=$(date +%s)
    echo "[$time] $@"
}

_load_env() {
    source env/$ENV
}

_setup_venv() {
    if [ -d $VENV_DIR ]; then
        _log "virtual environment already exists"
        return
    fi

    python3.12 -m venv $VENV_DIR
}

_activate_venv() {
    source $VENV_DIR/bin/activate
}

install() {
    _setup_venv
    _activate_venv

    pip install --force-reinstall -e ".[$ENV]"
}

sync() {
    _load_env
    _activate_venv
    python -m rtsw.persist.query "$@"
}

db_manage() {
    _load_env
    _activate_venv
    python -m rtsw.persist.manage "$@"
}

start_services() {
    docker compose up -d postgres
}

serve() {
    _load_env
    _activate_venv
    python -m rtsw.web
}

"$@"

#!/bin/bash

set -e

STACK_FILE="${STACK_FILE:-mirror.yml}"
STACK_NAME="${STACK_NAME:-rpmMirrorStack}"

_log() {
    echo "[$(date +'%H:%M:%S')]: $*"
}

validate-template() {
    aws cloudformation validate-template \
        --template-body "file://$(pwd)/${STACK_FILE}" \
        --output yaml
}

stack-exists() {
    aws cloudformation describe-stacks \
        --stack-name "${STACK_NAME}" \
        --output yaml >/dev/null && return 0 || return 1
}

delete-stack() {
    aws cloudformation delete-stack --stack-name "${STACK_NAME}"
    _log "deleting stack ${STACK_NAME}..."

    aws cloudformation wait stack-delete-complete --stack-name "${STACK_NAME}"
    _log "stack ${STACK_NAME} deleted"
}

create-stack() {
    local SSHLOCATION="${SSHLOCATION:-$(curl -s ipinfo.io/ip)/32}"
    local KEYNAME="${KEYNAME:-temp-key-pair}"

    local params=(
        "ParameterKey=KeyName,ParameterValue=${KEYNAME}"
        "ParameterKey=SSHLocation,ParameterValue=${SSHLOCATION}"
        "ParameterKey=RHELUser,ParameterValue=${RHEL_USER}"
        "ParameterKey=RHELPassword,ParameterValue=${RHEL_PASSWORD}"
    )

    aws cloudformation create-stack \
        --stack-name "${STACK_NAME}" \
        --template-body "file://$(pwd)/${STACK_FILE}" \
        --parameters "${params[@]}" \
        --disable-rollback >/dev/null

    _log "creating stack ${STACK_NAME}..."

    aws cloudformation wait stack-create-complete --stack-name "${STACK_NAME}"

    _log "stack ${STACK_NAME} created"
}

recreate-stack() {
    if stack-exists; then
        _log "stack ${STACK_NAME} exists, it will be deleted"
        delete-stack
    fi

    create-stack
}

"$@"

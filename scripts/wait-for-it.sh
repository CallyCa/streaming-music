#!/usr/bin/env bash
# Use this script to test if a given TCP host/port are available

# Copyright 2016, Bryan Dowling
# https://github.com/vishnubob/wait-for-it

# Licensed under the MIT License

set -e

TIMEOUT=15
QUIET=0
HOST="$1"
PORT="$2"

usage()
{
    cat << USAGE >&2
Usage:
    $0 host:port [-t timeout] [-- command args]
    -h HOST | --host=HOST       Host or IP under test
    -p PORT | --port=PORT       TCP port under test
                                Alternatively, you specify the host and port as host:port
    -t TIMEOUT | --timeout=TIMEOUT
                                Timeout in seconds, zero for no timeout
    -q | --quiet                Don't output any status messages
    -- COMMAND ARGS             Execute command with args after the test finishes
USAGE
    exit 1
}

wait_for()
{
    for i in `seq $TIMEOUT` ; do
        nc -z "$HOST" "$PORT" > /dev/null 2>&1 && break
        echo "Waiting for $HOST:$PORT..."
        sleep 1
    done
}

while [ $# -gt 0 ]
do
    case "$1" in
        *:* )
        HOST=$(printf "%s\n" "$1"| cut -d : -f 1)
        PORT=$(printf "%s\n" "$1"| cut -d : -f 2)
        shift 1
        ;;
        -h)
        HOST="$2"
        if [ "$HOST" == "" ]; then break; fi
        shift 2
        ;;
        --host=*)
        HOST="${1#*=}"
        shift 1
        ;;
        -p)
        PORT="$2"
        if [ "$PORT" == "" ]; then break; fi
        shift 2
        ;;
        --port=*)
        PORT="${1#*=}"
        shift 1
        ;;
        -t)
        TIMEOUT="$2"
        if [ "$TIMEOUT" == "" ]; then break; fi
        shift 2
        ;;
        --timeout=*)
        TIMEOUT="${1#*=}"
        shift 1
        ;;
        -q | --quiet)
        QUIET=1
        shift 1
        ;;
        --)
        shift
        break
        ;;
        -*)
        echo "Unknown option: $1" >&2
        usage
        ;;
        *)
        break
        ;;
    esac
done

if [ "$HOST" == "" -o "$PORT" == "" ]; then
    echo "Error: you need to provide a host and port to test."
    usage
fi

wait_for

shift

if [ "$QUIET" -ne 1 ]; then echo "$HOST:$PORT is available"; fi

exec "$@"

#!/usr/bin/env bash
set -Eeuo pipefail

usage() {
  printf 'Usage: %s https://service.example/healthz\n' "${0##*/}" >&2
}

die() {
  printf 'error: %s\n' "$*" >&2
  exit 2
}

if [[ $# -ne 1 ]]; then
  usage
  exit 2
fi

url=$1
[[ "$url" == https://* ]] || die "URL must use HTTPS"
command -v curl >/dev/null 2>&1 || die "curl is required"

if curl --fail --silent --show-error --max-time 5 --output /dev/null "$url"; then
  printf 'healthy: %s\n' "$url"
else
  status=$?
  printf 'health check failed (curl exit %s)\n' "$status" >&2
  exit 1
fi

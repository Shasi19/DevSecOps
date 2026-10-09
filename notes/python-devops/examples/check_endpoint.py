#!/usr/bin/env python3
"""Bounded HTTP health-check example with explicit exit status."""

import argparse
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument("--timeout", type=float, default=3.0)
    parser.add_argument("--expected-status", type=int, default=200)
    args = parser.parse_args()

    parsed = urlparse(args.url)
    if parsed.scheme != "https" or not parsed.hostname:
        parser.error("url must be an absolute HTTPS URL")
    if not 0 < args.timeout <= 30:
        parser.error("--timeout must be greater than 0 and at most 30 seconds")

    request = Request(args.url, headers={"User-Agent": "devsecops-health-check/1.0"})
    try:
        with urlopen(request, timeout=args.timeout) as response:
            if urlparse(response.geturl()).scheme != "https":
                print("health check redirected away from HTTPS", file=sys.stderr)
                return 2
            status = response.status
    except HTTPError as error:
        status = error.code
    except (URLError, TimeoutError, OSError) as error:
        print(f"health check failed: {type(error).__name__}", file=sys.stderr)
        return 2

    if status != args.expected_status:
        print(
            f"unexpected HTTP status: expected {args.expected_status}, got {status}",
            file=sys.stderr,
        )
        return 1
    print(f"healthy: HTTP {status}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

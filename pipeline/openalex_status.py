"""Say whether OpenAlex is accepting our calls, and why not.

Run this when fetch_openalex.py reports failures. It makes one cheap request
and prints the rate-limit headers, which tell apart three cases:
an accepted API credential, an anonymous call, and a spent daily budget.

Usage: python pipeline/openalex_status.py
"""
import json
import sys
import urllib.error
import urllib.request

from common import API_KEY_ENV_NAME, USER_AGENT

URL = "https://api.openalex.org/works?per-page=1&select=id"
HEADERS = ["x-ratelimit-limit-usd", "x-ratelimit-remaining-usd", "x-ratelimit-reset", "retry-after"]


def main():
    req = urllib.request.Request(URL, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            status, headers = resp.status, resp.headers
    except urllib.error.HTTPError as err:
        status, headers = err.code, err.headers
    except OSError as err:
        print(f"OpenAlex unreachable: {err}")
        return 1

    seen = {h: headers.get(h) for h in HEADERS if headers.get(h)}
    print(f"status {status}")
    print(json.dumps(seen, indent=2) if seen else "no rate-limit headers returned")

    limit = seen.get("x-ratelimit-limit-usd")
    if status == 200:
        print("OK: OpenAlex accepted the request.")
        if limit and float(limit.strip("$")) < 0.5:
            print(f"Warning: the daily budget is only {limit}, which means the call was anonymous. "
                  "The API credential is not reaching OpenAlex.")
    elif status == 429:
        print("Rate limited. Either the daily budget is spent, or the call was anonymous.")
        print("Check the API credential on the cloud environment: allowed website api.openalex.org, "
              "header Authorization, prefix Bearer, value the raw key with no prefix in it. "
              f"An environment variable named {API_KEY_ENV_NAME} also works.")
    return 0 if status == 200 else 1


if __name__ == "__main__":
    sys.exit(main())

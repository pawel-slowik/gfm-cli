#!/usr/bin/env python3

import sys
import os.path
import json
import urllib.parse
import urllib.request
import argparse
from http import HTTPStatus
from typing import Iterable, Tuple


def gfm_to_html(markdown: str) -> str:
    return api_request(
        "POST",
        "https://api.github.com/markdown",
        json.dumps({"text": markdown}),
        HTTPStatus.OK,
    )


def api_request(method: str, url: str, data: str, expected_status: HTTPStatus) -> str:
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": os.path.basename(sys.argv[0]),
    }
    request = urllib.request.Request(url, data.encode("ascii"), headers, method=method)
    with urllib.request.urlopen(request) as response:
        status = response.code
        encoding = headers_encoding(response.getheaders())
        body = response.read().decode(encoding)
    if status != expected_status:
        raise RuntimeError(f"unexpected HTTP code: {status}, response: {body}")
    return body


def headers_encoding(headers: Iterable[Tuple[str, str]]) -> str:
    for (header_name, header_value) in headers:
        if header_name.lower() == "content-type":
            return header_value.split(";")[1].split("=")[1]
    raise ValueError()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert GitHub Flavored Markdown into HTML using GitHubs REST API.",
        usage="%(prog)s < input.md > output.html",
    )
    parser.parse_args()
    html = gfm_to_html(sys.stdin.read())
    print(html)


if __name__ == "__main__":
    main()

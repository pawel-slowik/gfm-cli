#!/usr/bin/env python3

import sys
import os.path
import json
import urllib.parse
import http.client
import argparse
from http import HTTPStatus
from typing import Iterable, Tuple, Mapping, Type


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
    response = http_request(method, url, headers, data)
    encoding = headers_encoding(response.getheaders())
    body = response.read().decode(encoding)
    if response.status != expected_status:
        raise RuntimeError(
            "unexpected HTTP code: %d, response: %s"
            % (response.status, body)
        )
    return body


def http_request(
        method: str,
        url: str,
        headers: Mapping[str, str],
        data: str
    ) -> http.client.HTTPResponse:

    def connection_class(scheme: str) -> Type[http.client.HTTPConnection]:
        scheme_class_map = {
            "http": http.client.HTTPConnection,
            "https": http.client.HTTPSConnection,
        }
        return scheme_class_map[scheme.lower()]

    def url_without_netloc(url: str) -> str:
        split = urllib.parse.urlsplit(url)
        return urllib.parse.urlunsplit(("", "", split.path, split.query, split.fragment))

    parts = urllib.parse.urlparse(url)
    connection = connection_class(parts.scheme)(parts.netloc)
    connection.request(method, url_without_netloc(url), body=data, headers=headers)
    return connection.getresponse()


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

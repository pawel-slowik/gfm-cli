# GitHub Flavored Markdown CLI renderer

This CLI script converts a [GitHub Flavored Markdown][gfm] document into HTML
using [GitHubs REST API][api].

[gfm]: https://github.github.com/gfm/
[api]: https://docs.github.com/en/rest/markdown

## Requirements

Python 3.x. Only the Python standard library is required, there's no need to
install any additional packages.

## Usage

	./gfm.py < input.md > output.html

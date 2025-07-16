# winzy-pdf-crop

[![PyPI](https://img.shields.io/pypi/v/winzy-pdf-crop.svg)](https://pypi.org/project/winzy-pdf-crop/)
[![Changelog](https://img.shields.io/github/v/release/sukhbinder/winzy-pdf-crop?include_prereleases&label=changelog)](https://github.com/sukhbinder/winzy-pdf-crop/releases)
[![Tests](https://github.com/sukhbinder/winzy-pdf-crop/workflows/Test/badge.svg)](https://github.com/sukhbinder/winzy-pdf-crop/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/sukhbinder/winzy-pdf-crop/blob/main/LICENSE)

Get images from pdf

## Installation

First [install winzy](https://github.com/sukhbinder/winzy) by typing

```bash
pip install winzy
```

Then install this plugin in the same environment as your winzy application.
```bash
winzy install winzy-pdf-crop
```
## Usage

To get help type ``winzy  pdfcrop --help``

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd winzy-pdf-crop
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
python -m pytest
```

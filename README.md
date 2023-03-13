# INDIpy

[![tests](https://github.com/wlatanowicz/indipy/actions/workflows/tests.yml/badge.svg)](https://github.com/wlatanowicz/indipy/actions/workflows/tests.yml)
[![pypi](https://img.shields.io/pypi/v/indipy)](https://pypi.org/project/indipy/)

INDIpy is an open source Python implementation of the INDI (Instrument Neutral Distributed Interface) protocol. It can be used to:
* implement custom device drivers which will be run as subprocess controlled by `indiserver` along with drivers included in [INDI Library](http://indilib.org)
* implement custom INDI server
* implement client software

## Examples

You can find docker-based examples [here](./docker-examples/).

## Quickstart

Quickstart tutorial can be found [here](./QUICKSTART.md).

## Resources

### General:

INDI Protocol white paper: http://www.clearskyinstitute.com/INDI/INDI.pdf

INDI Project: http://indilib.org

### Technical details:

Standard Properties: https://indilib.org/develop/developer-manual/101-standard-properties.html

Driver Interfaces: http://docs.indilib.org/drivers/driver-interface.html

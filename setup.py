from setuptools import find_packages, setup
from pathlib import Path


BUNDLES = (
    "websockets",
)

# -*- Installation Requires -*-


def strip_comments(l):
    return l.split('#', 1)[0].strip()


def _pip_requirement(req, *root):
    if req.startswith('-r '):
        _, path = req.split()
        return reqs(*root, *path.split('/'))
    return [req]


def _reqs(*f):
    path = (Path.cwd() / 'requirements').joinpath(*f)
    with path.open() as fh:
        reqs = [strip_comments(l) for l in fh.readlines()]
        return [_pip_requirement(r, *f[:-1]) for r in reqs if r]


def reqs(*f):
    return [req for subreq in _reqs(*f) for req in subreq]


def extras(*p):
    """Parse requirement in the requirements/extras/ directory."""
    return reqs('extras', *p)


def extras_require():
    """Get map of all extra requirements."""
    return {x: extras(x + '.txt') for x in BUNDLES}
    

setup(
    name="indipy",
    version="0.1",
    description="Python implementation of INDI server and client",
    url="http://github.com/wlatanowicz/indipy",
    author="Wiktor Latanowicz",
    author_email="indipy@wiktor.latanowicz.com",
    license="MIT",
    packages=find_packages(exclude=["test*", "devices"]),
    zip_safe=False,
    install_requires=reqs('base.txt'),
    tests_require=reqs('tests.txt'),
    extras_require=extras_require(),
)

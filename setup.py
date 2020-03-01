from setuptools import find_packages, setup

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
)

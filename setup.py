"""
Setup orch_serv
"""
import os
import pathlib
import re
from typing import Optional

from setuptools import setup

LIB_NAME = "orch_serv"
HERE = pathlib.Path(__file__)


def get_version() -> Optional[str]:
    """
      Method for getting the version of the library from the init file
    :requirements: version must be specified separately
        :good: __version__ = '0.0.1'
        :bad: __version__, __any_variable__ = '0.0.1', 'any_value'
    :return: version lib
    """
    root_lib = pathlib.Path(__file__).parent / LIB_NAME
    txt = (root_lib / "__init__.py").read_text("utf-8")
    txt = txt.replace("'", '"')
    try:
        version = re.findall(r'^__version__ = "([^"]+)"\r?$', txt, re.M)[0]
        return version
    except IndexError:
        raise RuntimeError("Unable to determine version.")


def get_packages():
    """
    Method for getting packages used in the lib
    """
    ignore = ["__pycache__"]

    list_sub_folders_with_paths = [
        x[0].replace(os.sep, ".")
        for x in os.walk(LIB_NAME)
        if x[0].split(os.sep)[-1] not in ignore
    ]
    return list_sub_folders_with_paths


setup(
    name=LIB_NAME,
    version=get_version(),
    description="Library for fast build service and interaction management",
    author="Denis Shchutkiy",
    long_description=open("README_PYPI.md").read(),
    long_description_content_type="text/markdown",
    author_email="denisshchutskyi@gmail.com",
    url="https://github.com/Shchusia/orchestrator_service/",
    packages=get_packages(),
    keywords=["pip", LIB_NAME],
    python_requires=">=3.8",
    install_requires=["pydantic==1.9.0"],
)

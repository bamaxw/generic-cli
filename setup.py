import os

from setuptools import setup, find_packages


def read(file_name):
    '''Read contents of file'''
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, file_name)
    with open(file_path, "rt") as file:
        return file.read()


setup(name="generic-cli",
      author="Maximus Wasylow",
      version='0.0.26',
      author_email="bamwasylow@gmail.com",
      description="Python API for remote jigsaw connections",
      long_description=read("README.md"),
      packages=find_packages(),
      python_requires=">=3.7",
      install_requires=['aiohttp', 'crossroads', 'tenacity'])

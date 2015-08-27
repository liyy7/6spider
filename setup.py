# Automatically created by: shub deploy

from setuptools import setup, find_packages

setup(
    name='sixspider',
    version='0.0.1',
    packages=find_packages(),
    entry_points={'scrapy': ['settings = sixspider.settings']},
)

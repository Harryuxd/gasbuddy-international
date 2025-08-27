from setuptools import setup, find_packages

setup(
    name="gasbuddy",
    version="0.3.8",
    packages=find_packages(),
    install_requires=[
        "aiohttp>=3.12.0",
        "backoff>=2.2.0",
        "attrs>=25.0.0",
    ],
)

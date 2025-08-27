"""
Setup script to install gasbuddy package locally for deployment
"""
from setuptools import setup, find_packages
import os

# Try to install py-gasbuddy from PyPI, fallback to local installation
try:
    setup(
        name="gasbuddy-international-api",
        version="1.0.0",
        packages=find_packages(),
        install_requires=[
            "Flask==3.1.2",
            "py-gasbuddy==0.3.8",  # Try PyPI first
            "requests==2.32.5",
            "gunicorn==23.0.0",
            "aiohttp==3.12.15",
            "backoff==2.2.1",
            "attrs==25.3.0",
            "Werkzeug==3.1.3",
        ],
        dependency_links=[
            "git+https://github.com/ubisoft/py-gasbuddy.git@v0.3.8#egg=py-gasbuddy-0.3.8"
        ],
    )
except Exception:
    # Fallback: try to install from git
    setup(
        name="gasbuddy-international-api",
        version="1.0.0",
        packages=find_packages(),
        install_requires=[
            "Flask==3.1.2",
            "requests==2.32.5",
            "gunicorn==23.0.0",
            "aiohttp==3.12.15",
            "backoff==2.2.1",
            "attrs==25.3.0",
            "Werkzeug==3.1.3",
        ],
        dependency_links=[
            "git+https://github.com/ubisoft/py-gasbuddy.git@v0.3.8#egg=gasbuddy"
        ],
    )

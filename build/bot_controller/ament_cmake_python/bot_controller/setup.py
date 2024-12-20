from setuptools import find_packages
from setuptools import setup

setup(
    name='bot_controller',
    version='0.0.0',
    packages=find_packages(
        include=('bot_controller', 'bot_controller.*')),
)

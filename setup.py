#!/usr/bin/env python
import telegramio
from setuptools import setup

setup(
    name='telegramio',
    version=telegramio.__version__,
    url='https://github.com/maffazi/telegramio',
    keywords='Asyncio Telegram Bot API',
    description='Python Asynchronous Telegram API',
    long_description='Asynchronous library for building bots on Telegram API',
    classifiers = [
        'Topic :: Internet',
        'Environment :: Web Environment',
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5'
    ],

    author='maffa',
    author_email='maffazi@gmail.com',

    license='MIT',
    packages=['telegramio'],
    install_requires=['aiohttp>=1.0.5'],
    include_package_data=False
)

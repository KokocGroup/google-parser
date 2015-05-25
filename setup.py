from setuptools import setup


VERSION = "0.0.8"

setup(
    name='google-parser',
    description="Convert html to snippets",
    version=VERSION,
    url='https://github.com/KokocGroup/google-parser',
    download_url='https://github.com/KokocGroup/google-parser/tarball/v{}'.format(VERSION),
    packages=['google_parser'],
    install_requires=[
        'pyquery==1.2.9',
        'lxml==3.4.4',
    ],
)

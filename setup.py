from setuptools import setup


VERSION = "0.0.88"

setup(
    name='google-parser',
    description="Convert html to snippets",
    version=VERSION,
    url='https://github.com/KokocGroup/google-parser',
    download_url='https://github.com/KokocGroup/google-parser/tarball/v{0}'.format(VERSION),
    packages=['google_parser', 'google_query'],
    install_requires=[],
)

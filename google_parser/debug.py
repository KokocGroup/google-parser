from pprint import pprint

from google_parser.google import GoogleJsonParser

with open('tests/data/2024-02-05.txt', 'r') as file:
    content = file.read()

parser = GoogleJsonParser(content)

pprint(parser.get_serp())

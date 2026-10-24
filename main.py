import argparse

from markdownify import markdownify
from openai import OpenAI
import requests

from auth import *


SOURCE_CV = 'https://pointbeing.net/cv/'

OAI_MODEL = 'gpt-4o-mini'


def fetch_source(source_url: str) -> str:
    '''Fetch source_url via HTTP, returning the content as Markdown'''
    response = requests.get(source_url, timeout=15)
    response.raise_for_status()
    return markdownify(response.text, heading_style='ATX')


def get_desc_url() -> str:
    parser = argparse.ArgumentParser()
    parser.add_argument('source_desc')
    args = parser.parse_args()
    return args.source_desc


def hello_openai() -> str:
    client = OpenAI(api_key=OAI_KEY)
    response = client.responses.create(
        model=OAI_MODEL,
        input='Say hello from Python in one short sentence.',
    )
    return response.output_text.strip()


md: str = fetch_source(SOURCE_CV)
# print(md)

# source_desc: str = fetch_source(get_desc_url())
# print(source_desc)

hello: str = hello_openai()
print(hello)


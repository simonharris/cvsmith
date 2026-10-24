import markdownify
import requests


SOURCE_CV = 'https://pointbeing.net/cv/'


def fetch_source(source_url: str) -> str:
    '''Fetch source_url via HTTP, returning the content as Markdown'''
    response = requests.get(source_url, timeout=15)
    response.raise_for_status()
    return markdownify.markdownify(response.text, heading_style='ATX')


md: str = fetch_source(SOURCE_CV)

print(md)



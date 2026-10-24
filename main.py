import argparse
from pathlib import Path

from markdownify import markdownify
from openai import OpenAI
import requests

from auth import *


SOURCE_CV = 'https://pointbeing.net/cv/'
OAI_MODEL = 'gpt-4o-mini'
PROMPTS_DIR = Path(__file__).resolve().parent / 'prompts'


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


def load_description(source: str) -> str:
    path = Path(source)
    if path.exists():
        return path.read_text(encoding='utf-8')
    return fetch_source(source)


def load_prompt(path: str | Path) -> str:
    return Path(path).read_text(encoding='utf-8')


def render_prompt(template: str, **values: str) -> str:
    rendered = template
    for key, value in values.items():
        rendered = rendered.replace(f'{{{{{key}}}}}', str(value))
    return rendered


def build_messages(cv_content: str, job_description: str) -> list[dict[str, str]]:
    system_prompt = load_prompt(PROMPTS_DIR / 'system.txt')
    user_template = load_prompt(PROMPTS_DIR / 'user.txt')
    user_prompt = render_prompt(
        user_template,
        cv_content=cv_content,
        job_description=job_description,
    )
    return [
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': user_prompt},
    ]


def generate_cv_match(cv_content: str, job_description: str) -> str:
    client = OpenAI(api_key=OAI_KEY)
    response = client.responses.create(
        model=OAI_MODEL,
        input=build_messages(cv_content, job_description), # type: ignore
    )
    return response.output_text.strip()


# def hello_openai() -> str:
#     client = OpenAI(api_key=OAI_KEY)
#     response = client.responses.create(
#         model=OAI_MODEL,
#         input='Say hello from Python in one short sentence.',
#     )
#     return response.output_text.strip()


if __name__ == '__main__':
    source_desc = get_desc_url()
    job_description = load_description(source_desc)
    cv_content = fetch_source(SOURCE_CV)
    print(generate_cv_match(cv_content, job_description))


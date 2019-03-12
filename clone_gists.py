"""Clone all Gists from GitHub."""

import os
import subprocess

import requests

GITHUB_ACCESS_TOKEN = os.getenv('GITHUB_ACCESS_TOKEN')
PER_PAGE = 100


def get_page(url: str):
    return requests.get(url, headers={'Authorization': f'token {GITHUB_ACCESS_TOKEN}'})


def clone_gist(gist: dict):
    _id = gist['id']
    description = gist['description'].replace('/', '-')

    if os.path.exists(os.path.join('gists', description)):
        return

    print(f'Cloning "{description}"...')

    try:
        subprocess.run(['git', 'clone', f'git@gist.github.com:{_id}.git'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(['mv', f'{_id}', f'gists/{description}'])
    except OSError as err:  # Ex. invalid directory name
        print(str(err))


def main():
    os.makedirs('gists', exist_ok=True)

    url = f'https://api.github.com/gists?per_page={PER_PAGE}'

    while True:
        resp = get_page(url)

        for gist in resp.json():
            clone_gist(gist)

        try:
            url = resp.links['next']['url']
        except KeyError:  # Last page
            break


if __name__ == "__main__":
    main()

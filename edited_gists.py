"""Check for any uncommited changes."""

import os
import subprocess


def main():
    if not os.path.exists('gists'):
        return

    gists_path = os.path.abspath('gists')

    for gist in os.listdir(gists_path):
        _path = os.path.join(gists_path, gist)

        try:
            subprocess.run(['git', 'diff', '--exit-code'], cwd=_path, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(['git', 'diff', '--cached', '--exit-code'], cwd=_path, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError:  # Non-zero exit code
            print(f'Uncommitted changes in "{gist}"')

        untracked_files = subprocess.check_output(['git', 'ls-files', '--other', '--exclude-standard', '--directory'], cwd=_path)
        if untracked_files:
            print(f'Untracked changes in "{gist}"')


if __name__ == "__main__":
    main()

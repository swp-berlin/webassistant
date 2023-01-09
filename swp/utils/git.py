import os
import subprocess


def get_commit(path, revision='HEAD'):
    if commit := os.environ.get('GITHUB_SHA'):
        return commit

    path = os.path.abspath(path)
    command = ['git', 'rev-parse', revision]

    if os.path.isfile(path):
        path = os.path.dirname(path)

    output = subprocess.check_output(command, cwd=path, encoding='utf-8')

    return str.strip(output)

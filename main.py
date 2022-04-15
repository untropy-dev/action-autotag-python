import os
from pathlib import Path

from github import Github


def main():
    about = {}
    with Path(os.environ["INPUT_PATH"]).open() as f:
        exec(f.read(), about)

    prefix = os.environ["INPUT_PREFIX"]
    variable = os.environ["INPUT_VARIABLE"]
    suffix = os.environ["INPUT_SUFFIX"]
    version_tag = f"{prefix}{about[variable]}{suffix}"

    g = Github(os.environ["INPUT_GITHUB_TOKEN"])
    repo = g.get_repo(os.environ["GITHUB_REPOSITORY"])

    for tag in repo.get_tags():
        if tag.name == version_tag:
            return

    sha = os.environ["GITHUB_SHA"]
    repo.create_git_ref(f"refs/tags/{version_tag}", sha)


if __name__ == "__main__":
    main()

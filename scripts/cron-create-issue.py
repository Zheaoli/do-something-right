from os import name
from typing import Optional
from pydantic import BaseSettings
from datetime import datetime
import github


class Settings(BaseSettings):
    GITHUB_TOKEN: Optional[str] = None
    REPO_NAME: Optional[str] = None


SETTINGS = Settings()

GITHUB_CLIENT = github.Github(SETTINGS.GITHUB_TOKEN)


def main():
    now = datetime.now().strftime("%Y-%m-%d")
    repo = GITHUB_CLIENT.get_repo(SETTINGS.REPO_NAME)
    try:
        label = repo.get_label(now)
    except github.GithubException as e:
        if e.status == 404:
            label = None
        else:
            raise e
    if not label:
        label = repo.create_label(now, "ffffff", f"{now}")
    issues = repo.get_issues(
        state="open", sort="created", direction="asc", labels=[label.name]
    )
    if issues.totalCount == 0:
        repo.create_issue(f"{now}", f"{now}", labels=[label.name])


if __name__ == "__main__":
    main()

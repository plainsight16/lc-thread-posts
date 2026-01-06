import os
import requests
from launch_editor import open_editor

GITHUB_API = "https://api.github.com/gists"


def create_gist(title, content, public=True, filename=None):
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("Missing GITHUB_TOKEN")

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
    }

    filename = filename or f"{title.replace(' ', '_')}.md"

    payload = {
        "description": title,
        "public": public,
        "files": {
            filename: {
                "content": content
            }
        },
    }

    response = requests.post(GITHUB_API, json=payload, headers=headers)
    response.raise_for_status()

    return response.json()["html_url"]

def create_gist_from_editor(title):
    content = open_editor(
        initial_text=f"# {title}\n\n",
        suffix=".md"
    )

    if not content.strip():
        raise ValueError("Empty markdown file")

    return create_gist(
        title=title,
        content=content,
        filename="solution.md",
        public=True
    )


def post_gist(problem, solution) -> str | None:
    gist_url:str| None = create_gist(
    title=f"LeetCode – {problem}",
    content=solution,
    public=True,
    filename="solution.md"
    )
    return gist_url

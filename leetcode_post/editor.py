import os
import tempfile
import subprocess


def open_editor(template:str, initial_text="", suffix=".md", ):
    editor = os.getenv("EDITOR")
    if not editor:
        raise RuntimeError("EDITOR environment variable not set")

    with tempfile.NamedTemporaryFile(
        mode="w+",
        suffix=suffix,
        delete=False
    ) as f:
        content = template.format(initial_text)
        f.write(content)
        f.flush()
        path = f.name

    subprocess.call(editor.split() + [path])

    with open(path, "r") as f:
        content = f.read()

    os.unlink(path)
    return content
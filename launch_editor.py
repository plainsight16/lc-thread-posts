import os
import tempfile
import subprocess


def open_editor(initial_text="", suffix=".md"):
    editor = os.getenv("EDITOR")
    if not editor:
        raise RuntimeError("EDITOR environment variable not set")

    with tempfile.NamedTemporaryFile(
        mode="w+",
        suffix=suffix,
        delete=False
    ) as f:
        f.write(initial_text)
        f.flush()
        path = f.name

    subprocess.call(editor.split() + [path])

    with open(path, "r") as f:
        content = f.read()

    os.unlink(path)
    return content
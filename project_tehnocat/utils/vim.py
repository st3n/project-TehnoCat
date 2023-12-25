import subprocess
import tempfile
import os


def edit_note_with_vim(note_content):
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmpfile:
        tmpfile_name = tmpfile.name
        tmpfile.write(note_content)

    subprocess.run(["vim", tmpfile_name])

    with open(tmpfile_name, "r") as tmpfile:
        updated_content = tmpfile.read()

    os.remove(tmpfile_name)

    return updated_content

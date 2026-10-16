
import json
import os


def write_files(files):
    old_files = {}

    try:
        for file_path, content in files:
            file_path = os.path.abspath(file_path)

            if file_path not in old_files:
                if os.path.exists(file_path):
                    with open(file_path, "r", encoding="utf-8", newline="") as file:
                        old_files[file_path] = (True, file.read())
                else:
                    old_files[file_path] = (False, None)

            directory = os.path.dirname(file_path)
            os.makedirs(directory, exist_ok=True)

            with open(file_path, "w", encoding="utf-8", newline="") as file:
                file.write(content)

    except (OSError, UnicodeError, TypeError):
        for file_path, old_data in reversed(list(old_files.items())):
            existed, content = old_data

            try:
                if existed:
                    with open(file_path, "w", encoding="utf-8", newline="") as file:
                        file.write(content)
                elif os.path.exists(file_path):
                    os.remove(file_path)
            except OSError:
                pass

        raise

def write_json_files(files):
    contents = []

    for file_path, data in files:
        content = json.dumps(
            data,
            ensure_ascii=False,
            indent=2,
            allow_nan=False
        )
        contents.append((file_path, content))

    write_files(contents)
import json
import os
import shutil
import tempfile


def write_files(files):
    pending = []
    completed = []
    temporary_files = []
    try:
        for file_path, content in files:
            file_path = os.path.abspath(file_path)
            directory = os.path.dirname(file_path)
            os.makedirs(directory, exist_ok=True)
            descriptor, temporary_path = tempfile.mkstemp(dir=directory, suffix=".tmp")
            os.close(descriptor)
            temporary_files.append(temporary_path)
            with open(temporary_path, "w", encoding="utf-8", newline="") as file:
                file.write(content)

            backup_path = None
            if len(files) > 1 and os.path.exists(file_path):
                descriptor, backup_path = tempfile.mkstemp(dir=directory, suffix=".bak")
                os.close(descriptor)
                temporary_files.append(backup_path)
                shutil.copyfile(file_path, backup_path)
            pending.append((file_path, temporary_path, backup_path))

        for file_path, temporary_path, backup_path in pending:
            os.replace(temporary_path, file_path)
            completed.append((file_path, backup_path))
    except OSError:
        restore_errors = []
        for file_path, backup_path in reversed(completed):
            if backup_path is not None:
                temporary_files.remove(backup_path)
            try:
                if backup_path is None:
                    os.remove(file_path)
                else:
                    os.replace(backup_path, file_path)
            except OSError:
                restore_errors.append(file_path + "; backup: " + str(backup_path))
        if restore_errors:
            raise OSError("Could not restore: " + ", ".join(restore_errors))
        raise
    finally:
        for temporary_path in temporary_files:
            try:
                os.remove(temporary_path)
            except OSError:
                pass


def write_json_files(files):
    contents = []
    for file_path, data in files:
        contents.append((file_path, json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False)))
    write_files(contents)

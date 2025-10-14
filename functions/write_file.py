import os
from google.genai import types


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="write contents to a file, create one if it does not exist.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to a specific file",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The contents to be written to the file"
            ),
        },
    ),
)


def write_file(working_directory, file_path, content):
    # collapse any use of .. or .
    abs_working = os.path.abspath(working_directory)
    # combine directory and file path while collapsing .. or .
    abs_given = os.path.abspath(os.path.join(working_directory, file_path))

    # add os correct separator to end of URI
    work_prefix = os.path.join(abs_working, "")

    # a descendant of allowed directory
    if not (abs_given.startswith(work_prefix)):
        return (f'Error: Cannot write "{file_path}" '
                f'as it is outside the permitted working directory.')

    # ensure a file was passed and not a dir
    if os.path.isdir(abs_given):
        return f'Error: "{file_path}" is a directory, not a file path'

    # ensure parent directory exists
    parent_dir = os.path.dirname(abs_given)
    if parent_dir and not os.path.exists(parent_dir):
        try:
            os.makedirs(parent_dir, exist_ok=True)
        except Exception:
            return f'Error: makedirs for "{file_path}" failed.'
    # try to write to file or create file
    try:
        with open(abs_given, "w", encoding="utf-8") as f:
            f.write(content)
        return (f'Successfully wrote to "{file_path}" ({len(content)} '
                f'characters written)')
    except Exception:
        return f'Error: write to "{file_path}" failed.'

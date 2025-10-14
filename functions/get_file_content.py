import os
from google.genai import types
MAX_CHARS = 10000

schema_get_file_contents = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the contents of a file up to a MAX_CHARS value.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to a specific file",
            ),
        },
    ),
)


def get_file_content(working_directory, file_path):
    abs_working = os.path.abspath(working_directory)
    abs_given = os.path.abspath(os.path.join(working_directory, file_path))

    work_prefix = os.path.join(abs_working, "")

    if not (abs_given == abs_working or abs_given.startswith(work_prefix)):
        return (f'Error: Cannot read "{file_path}"'
                f'as it is outside the permitted working directory.')

    if not os.path.isfile(abs_given):
        return (f'Error: File not found or is not a regular file:'
                f'"{file_path}"')
    try:
        with open(abs_given, "r", encoding="utf-8") as f:

            file_content_string = f.read()
            if len(file_content_string) > MAX_CHARS:
                return (f'{file_content_string[:MAX_CHARS]} File "{file_path}"'
                        f'truncated at {MAX_CHARS} characters')
            return file_content_string
    except FileNotFoundError:
        return "Error: unable to open file"

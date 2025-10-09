import os

MAX_CHARS = 10000


def get_file_content(working_directory, file_path):
    abs_working = os.path.abspath(working_directory)
    abs_given = os.path.abspath(os.path.join(working_directory, file_path))

    work_prefix = os.path.join(abs_working, "")

    if not (abs_given == abs_working or abs_given.startswith(work_prefix)):
        return (f'Error: Cannot read "{file_path}" as it is outside the permitted working directory.')

    if not os.path.isfile(abs_given):
        return (f'Error: File not found or is not a regular file: "{file_path}"')
    try:
        with open(abs_given, "r", encoding="utf-8") as f:

            file_content_string = f.read()
            if len(file_content_string) > MAX_CHARS:
                return f'{file_content_string[:MAX_CHARS]} File "{file_path}" truncated at {MAX_CHARS} characters'
            return file_content_string
    except FileNotFoundError:
        return "Error: unable to open file"

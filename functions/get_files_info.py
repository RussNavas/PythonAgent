import os
from google.genai import types


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="""The directory to list files from,
                relative to the working directory. If not provided,
                 lists files in the working directory itself."""
            ),
        },
    ),
)


def get_files_info(working_directory, directory="."):

    abs_working = os.path.abspath(working_directory)
    abs_given = os.path.abspath(os.path.join(working_directory, directory))

    work_prefix = os.path.join(abs_working, "")

    if not (abs_given == abs_working or abs_given.startswith(work_prefix)):
        return (f'Error: Cannot list "{directory}"'
                f'as it is outside the permitted working directory.')

    if not os.path.isdir(abs_given):
        return f'Error: "{directory}" is not a directory'

    entries = os.listdir(abs_given)

    res_header = "Result for current directory: "
    res_strings = []
    for entry in entries:
        file_path = os.path.join(abs_given, entry)
        is_dir = os.path.isdir(file_path)
        file_size = os.path.getsize(file_path)
        name = entry
        res_string = f"- {name}: file_size={file_size} bytes, is_dir={is_dir}"
        res_strings.append(res_string)

    return (f"{res_header}\n" + "\n".join(res_strings))

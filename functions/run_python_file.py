import os
import sys
import subprocess


def run_python_file(working_directory, file_path, args=[]):
    abs_working = os.path.abspath(working_directory)
    abs_given = os.path.abspath(os.path.join(working_directory, file_path))

    work_prefix = os.path.join(abs_working, "")

    if not (abs_given.startswith(work_prefix)):
        return (f'Error: Cannot execute "{file_path}" as it is outside'
                f'the permitted working directory.')

    if not os.path.exists(abs_given):
        return f'Error: File "{file_path}" not found.'

    if file_path[-3:] != ".py":
        return f'Error: "{file_path}" is not a Python file.'

    # workaround to ensure scripts can run mac or windows
    # without shebang etc.
    cmd = [sys.executable, abs_given, *map(str, args)]
    try:
        result = subprocess.run(cmd,
                                cwd=abs_working,
                                timeout=30,
                                capture_output=True,
                                text=True)
        result_stdout = result.stdout
        result_stderr = result.stderr
        res_string = (f'STDOUT: {result_stdout}\n'
                      f'STDERR: {result_stderr}\n')

        if result.returncode != 0:
            res_string += f"Process exited with code {result.returncode}"
        if not res_string:
            return "No output produced"
        return res_string
    except Exception as e:
        return f"Error: executing Python file: {e}"

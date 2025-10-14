from google.genai import types
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file


def call_function(function_call_part, verbose=False):
    
    function_name = function_call_part.name
    function_args = function_call_part.args or {}

    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    function_args["working_directory"] = "./calculator"

    if function_name == "run_python_file" and not function_args.get("args"):
        function_args["args"] = []

    if function_name == "get_files_info":
        function_result = get_files_info(**function_args)

    elif function_name == "get_file_content":
        function_result = get_file_content(**function_args)

    elif function_name == "write_file":
        function_result = write_file(**function_args)

    elif function_name == "run_python_file":
        function_result = run_python_file(**function_args)

    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"unknown function: {function_name}"},
                )
            ],
        )

    return types.Content(
        role="user",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ]
    )

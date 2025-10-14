import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.call_function import call_function
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_contents
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file

load_dotenv()

# get api key from .env
api_key = os.environ.get("GEMINI_API_KEY")
# pass api key to new instance of Gemini client
client = genai.Client(api_key=api_key)

# from boot.dev
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan.
You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory.
You do not need to specify the working directory in your function calls as it
is automatically injected for security reasons

When a listed tool can satisfy the request, 
call it directly without asking for confirmation.
If arguments are unspecified for run_python_file, 
use an empty list [] for args.
When fixing a bug in code, always locate and modify the relevant 
file in the working directory (e.g., calculator.py)
instead of creating a new file like main.py.
"""


# a list of available functions:
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_contents,
        schema_write_file,
        schema_run_python_file,
    ]
)


def main():
    prompt = None
    if len(sys.argv) > 1:
        prompt = sys.argv[1]
    if not prompt:
        print("Error: Please Provide a Prompt")
        sys.exit(1)

    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]

    for _ in range(20):
        response = client.models.generate_content(
            model='gemini-2.0-flash-001',  # chosen model
            contents=messages,  # payload from user
            #  list of available functions and the user prompt
            config=types.GenerateContentConfig(tools=[available_functions],
                                            system_instruction=system_prompt),
        )
        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)

        if response.function_calls and len(response.function_calls) > 0:
            for call in response.function_calls:
                function_call_result = call_function(call,
                                                     verbose="--verbose" in sys.argv)
                
                valid = (
                    function_call_result.parts and
                    hasattr(function_call_result.parts[0], "function_response")
                )
                if not valid:
                    raise RuntimeError("Fatal: function call did not"
                                       + "return a function_response")

                messages.append(function_call_result)

                if "--verbose" in sys.argv:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
            continue

        if not response.function_calls and response.text:
            print(f"{response.text}")
            break


if __name__ == "__main__":
    main()

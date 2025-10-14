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
    response = client.models.generate_content(
        model='gemini-2.0-flash-001',  # chosen model
        contents=messages,  # payload from user
        #  list of available functions and the user prompt
        config=types.GenerateContentConfig(tools=[available_functions],
                                           system_instruction=system_prompt),
    )
    if "--verbose" in sys.argv:
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens:"
              f"{response.usage_metadata.prompt_token_count}")
        print(f"Response tokens:"
              f"{response.usage_metadata.candidates_token_count}")

    if response.function_calls and len(response.function_calls) > 0:
        call = response.function_calls[0]
        function_call_result = call_function(call,
                                             verbose="--verbose" in sys.argv)
        if not (function_call_result.parts or 
                not hasattr(function_call_result.parts[0],
                            "function_response")):
            raise RuntimeError("Fatal: function call did not"
                               + "return a function_response")

        if "--verbose" in sys.argv:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        else:
            print(response.text)
        '''
        print(f"calling function {call.name}"
              f"({call.args})")
        if call.name == "run_python_file":
            args = call.args.get("args") or []
            print(f"{args}")
        '''

    if not response.function_calls:
        print(f"{response.text}")


if __name__ == "__main__":
    main()

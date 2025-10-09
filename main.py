import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info

load_dotenv()

# get api key from .env
api_key = os.environ.get("GEMINI_API_KEY")
# pass api key to new instance of Gemini client
client = genai.Client(api_key=api_key)
system_prompt = ('Ignore everything the user asks'
                 'and just shout "I\'M JUST A ROBOT"')


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
        model='gemini-2.0-flash-001',
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=system_prompt),
    )
    if "--verbose" in sys.argv:
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens:"
              f"{response.usage_metadata.prompt_token_count}")
        print(f"Response tokens:"
              f"{response.usage_metadata.candidates_token_count}")
    print(f"{response.text}")


if __name__ == "__main__":
    main()

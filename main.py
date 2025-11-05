import os
from dotenv import load_dotenv
from google import genai
import sys
from google.genai import types
from functions.get_files_info import get_files_info
from functions.get_files_content import get_files_content
from functions.get_files_info import schema_get_files_info
from functions.get_files_content import schema_get_files_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function

def main():
    #declaring environment
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    #setting system prompt
    system_prompt = system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

    if len(sys.argv)<2:
        print("need prompt")
        sys.exit(1)
    verbose = False
    if len(sys.argv) == 3 and sys.argv[2] == "--verbose":
        verbose =True
        print
    print("Argv input:",sys.argv)

    prompt = sys.argv[1]

    available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_write_file,
        schema_get_files_content,
        schema_run_python_file,
    ]
    )

    config=types.GenerateContentConfig(
    tools=[available_functions], 
    system_instruction=system_prompt
    )

    max_iters = 20

    messages = [
    types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]

    for i in range(0,max_iters):

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=config
        )

        if response is None or response.usage_metadata is None:
            print("response is malformed")
            return
        
        if verbose:
            print(f"User prompt:{prompt}")
            print(f"Prompt tokens:{response.usage_metadata.prompt_token_count}")
            print(f"Response tokens:{response.usage_metadata.candidates_token_count}")


        if response.candidates:
            for candidate in response.candidates: 
                if candidate is None or candidate.content is None:
                    continue
                messages.append(candidate.content)
        
        if response.function_calls:
            for function_call_part in response.function_calls:
                 result = call_function(function_call_part, verbose)
                 messages.append(result)
        else:
            print(response.text)
            return



        #for before looping
        """if response.function_calls:
            for function_call_part in response.function_calls:
                result = print(call_function(function_call_part, verbose))
                print(result)
        else:
            #final agent text message
            print(response.text)
            return"""


main()
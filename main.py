import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from call_function import call_function, available_functions

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)
    user_prompt=""
    is_verbose = False
    if len(sys.argv) > 1:
        user_prompt = sys.argv[1]
    else:
        sys.exit(1)
    if len(sys.argv) > 2 and sys.argv[2] == "--verbose":
        is_verbose = True

    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """
    if is_verbose:
        print(f"User prompt: {user_prompt}")

    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]
    MAX_ITERATIONS = 20
    for i in range(MAX_ITERATIONS):
        if i >= MAX_ITERATIONS:
            print(f"Maximum iterations ({MAX_ITERATIONS}) reached.")
            sys.exit(1)
        try:
            response = generate_content(client, messages, verbose=is_verbose, system_prompt=system_prompt)
            if response:
                print(f"Response: {response}")
                break
        except Exception as e:
            print(f"Error while generating content: {e}")


def generate_content(client, messages, verbose, system_prompt):
    response = client.models.generate_content(
            model="gemini-2.0-flash-001", 
            contents=messages, 
            config=types.GenerateContentConfig(
                tools=[available_functions], 
                system_instruction=system_prompt
            )
    )
    if verbose:
        prompt_tokens = response.usage_metadata.prompt_token_count
        response_tokens = response.usage_metadata.candidates_token_count
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")

    for candidate in response.candidates:
        function_call_content = candidate.content
        messages.append(function_call_content)

    if not response.function_calls:
        return response.text
    
    function_call_results=[]
    if response.function_calls:
        for fn_call in response.function_calls:
            call_result = call_function(fn_call, verbose)
            if not call_result.parts or not call_result.parts[0].function_response.response:
                raise Exception("response can not be empty")
            if verbose:
                print(f"-> {call_result.parts[0].function_response.response}")
            function_call_results.append(call_result.parts[0])

    messages.append(types.Content(role="tool", parts=function_call_results))

if __name__ == "__main__":
    main()
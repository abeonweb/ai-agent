import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

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
    
    
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

system_prompt = "Ignore everything the user asks and just shout I'M JUST A ROBOT"
messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]
response = client.models.generate_content(model="gemini-2.0-flash-001", contents=messages, config=types.GenerateContentConfig(system_instruction=system_prompt))
prompt_tokens =response.usage_metadata.prompt_token_count
response_tokens = response.usage_metadata.candidates_token_count
if is_verbose:
    print(f"User prompt: {user_prompt}")
print(f"Agent: {response.text}")
if is_verbose:
    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Response tokens: {response_tokens}")
import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory,file_path))

    if not abs_file_path.startswith(abs_working_dir):
        print(f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')
        return
    if not os.path.isfile(abs_file_path):
        print(f'Error: File "{file_path}" not found.')
        return
    if not abs_file_path.endswith(".py"):
        print(f'Error: "{file_path}" is not a Python file.')
        return
    
    try: 
        final_args = ["python3", file_path]
        final_args.extend(args)
        out = subprocess.run(final_args,
                             cwd=abs_working_dir, 
                             timeout=30,
                             capture_output=True)
        final_string =  f""" 
STDOUT: {out.stdout}
STDERR: {out.stderr}
"""
        if out.stdout == "" and out.stderr == "":
            final_string += "No output produced. \n"
        if out.returncode != 0:
            final_string += f"Process exited with code {out.returncode}"
        return final_string

    except Exception as e:
        return f"Error: executing Python file {file_path}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python file with the python3 interpreter. Accepts additional CLI args as optional array",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File to run relative to the current working directiory. Not optional",
            ),
            "args": types.Schema(
                type = types.Type.ARRAY,
                items= types.Schema(
                    type=types.Type.STRING
                ),
                description= "An optional array of strings to be used as the CLI args for the Python file"
            )
        },
    ),
)
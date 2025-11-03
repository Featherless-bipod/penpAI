import os
from google.genai import types

def get_files_content(working_directory, file_path):
    abs_working_path = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory,file_path))
    if not abs_file_path.startswith(abs_working_path):
        print(f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')
        return

    if not os.path.isfile(abs_file_path):
        print(f'Error: File not found or is not a regular file: "{file_path}"')
        return
    
    max_char = 10000
    with open(abs_file_path,"r") as f: 
        file_content_string = f.read(max_char)
        
    if len(file_content_string) == max_char:
        file_content_string += f'File "{file_path}" truncated at 10000 characters'
    return file_content_string
    

schema_get_files_content = types.FunctionDeclaration(
    name="get_files_content",
    description="Gets the contents of the given file as a string, constrained to a working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file, from the working directory. Not optional"
            ),
        },
    ),
)
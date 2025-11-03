import os
from google.genai import types


def get_files_info(working_directory, directory="."):
    abs_working_dir = os.path.abspath(working_directory) #the parameter directory
    abs_directory = os.path.abspath(os.path.join(working_directory,directory)) #directory llm is in
    if not abs_directory.startswith(abs_working_dir): #if the llmdir is not in the paramters
        return f'Error: "{directory}" is not in working directory' #say that it is off limits
    
    final_response = ""
    contents = os.listdir(abs_directory) #if the file is in parameters, find the contents you want
    for content in contents: #for each content 
        content_path = os.path.join(abs_directory,content) #join the path and the file name so that you get the path to the file
        is_dir = os.path.isdir(content_path) #is file or directory(folder)
        size = os.path.getsize(content_path) #what is file size 
        final_response += f"- {content}: file_size = {size} bytes, is dir = {is_dir}\n"
    
    return final_response


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


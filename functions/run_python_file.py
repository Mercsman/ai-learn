import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file relative to the working directory, optionally with command-line arguments",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional list of command-line arguments to pass to the Python file",
            ),
        },
        required=["file_path"],
    ),
)



def run_python_file(working_directory, file_path, args=None):
    try:
        if args is None:
            args = []

        # Absolute working directory
        working_dir_abs = os.path.abspath(working_directory)

        # Build and normalize absolute file path
        absolute_file_path = os.path.normpath(
            os.path.join(working_dir_abs, file_path)
        )

        # Guardrail: ensure file is inside working directory
        if os.path.commonpath([working_dir_abs, absolute_file_path]) != working_dir_abs:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        # Must exist and be a regular file
        if not os.path.isfile(absolute_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        # Must be a Python file
        if not absolute_file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        # Build command
        command = ["python", absolute_file_path]
        if args:
            command.extend(args)

        # Run subprocess
        completed = subprocess.run(
            command,
            cwd=working_dir_abs,
            capture_output=True,
            text=True,
            timeout=30,
        )

        output_parts = []

        if completed.returncode != 0:
            output_parts.append(f"Process exited with code {completed.returncode}")

        if completed.stdout:
            output_parts.append(f"STDOUT:\n{completed.stdout}")

        if completed.stderr:
            output_parts.append(f"STDERR:\n{completed.stderr}")

        if not completed.stdout and not completed.stderr:
            output_parts.append("No output produced")

        return "\n".join(output_parts)

    except Exception as e:
        return f"Error: executing Python file: {e}"

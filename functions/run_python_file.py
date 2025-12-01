from pathlib import Path
import subprocess
import os
from typing import List, Optional

def run_python_file(working_directory: str, file_path: str, args: Optional[List[str]] = None) -> str:
    """
    Execute a python file using the 'python' command.

    Returns a string formatted with:
      STDOUT: <stdout>
      STDERR: <stderr>
    If the process exits with a non-zero code, appends:
      PRocess exited with code X
    If no output was produced, returns "No  output produced."
    On any validation or runtime error, returns an error string.
    """
    if args is None:
        args = []

    try:
        wd_resolved = Path(working_directory).resolve()
        fp_resolved = (wd_resolved / file_path).resolve()
    except Exception as e:
        return f"Error resolving paths: {e}"

    # Ensure file_path is inside working_directory
    try:
        # Use commonpath to avoid false positives with similar prefixes
        if os.path.commonpath([str(wd_resolved), str(fp_resolved)]) != str(wd_resolved):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    except Exception as e:
        return f"Error checking path containment: {e}"

    # Check file exists
    if not fp_resolved.exists():
        return f'Error: File "{file_path}" not found.'

    # Check .py extension
    if fp_resolved.suffix.lower() != ".py":
        return f'Error: "{file_path}" is not a Python file.'

    # Build command
    cmd = ["python", str(fp_resolved)] + list(args)

    try:
        completed_process = subprocess.run(
            cmd,
            timeout=30,
            capture_output=True,
            text=True,
            cwd=str(wd_resolved),
        )
    except Exception as e:
        return f"Error: executing Python file: {e}"

    stdout = completed_process.stdout or ""
    stderr = completed_process.stderr or ""

    if not stdout and not stderr:
        return "No  output produced."

    output_parts = [f"STDOUT: {stdout}", f"STDERR: {stderr}"]
    if completed_process.returncode != 0:
        output_parts.append(f"Process exited with code {completed_process.returncode}")

    return "\n".join(output_parts)

schema_run_python_file = {
    "name": "run_python_file",
    "description": "Run a Python file within the working directory and capture its output.",
    "parameters": {
        "type": "object",
        "properties": {
            "working_directory": {
                "type": "string",
                "description": "The base working directory from which to run the Python file.",
            },
            "file_path": {
                "type": "string",
                "description": "The relative path to the Python file within the working directory.",
            },
            "args": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Optional list of command-line arguments to pass to the Python file.",
            },
        },
        "required": ["file_path"],
    },
}
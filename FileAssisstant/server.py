from mcp.server import FastMCP
from pathlib import Path

mcp = FastMCP("FileAssisstant")

# Resolve workspace path relative to this script file
workspace = (Path(__file__).parent / "workspace").resolve()
workspace.mkdir(exist_ok=True, parents=True)


def get_safe_path(path: str):
    candidate = (workspace / path).resolve()
    if workspace not in candidate.parents and candidate != workspace:
        raise ValueError("Invalid Path")
    return candidate


@mcp.tool()
def list_files():
    """List all files and folders in the workspace."""

    items = [item.name for item in workspace.iterdir()]

    if not items:
        return "Workspace is empty."

    return items


@mcp.tool()
def read_file(path: str):
    """Read the contents of a file."""
    try:
        file_path = get_safe_path(path)
        if not file_path.exists():
            return "File not found"
        if not file_path.is_file():
            return "not a file"
        return file_path.read_text(encoding="utf-8")
    except ValueError as e:
        return str(e)
    except Exception as e:
        return str(e)


@mcp.tool()
def write_file(path: str, content: str):
    """Write content to a file."""
    try:
        file_path = get_safe_path(path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")
        return "File written successfully."
    except ValueError as e:
        return str(e)
    except Exception as e:
        return str(e)


@mcp.tool()
def delete_file(path:str):
    """deletes a file"""
    try:
        file_path = get_safe_path(path)
        if not file_path.exists():
            return "not found"
        if not file_path.is_file():
            return "not a file"
        file_path.unlink()
        return f"Deleted {path}"
    except Exception as e:
        return str(e)

@mcp.tool()
def create_dir(path:str):
    """creates a directory"""
    try:
        dir_path = get_safe_path(path)
        dir_path.mkdir(parents = True, exist_ok = True)
        return f"Directory '{path}' created"
    except Exception as e:
        return str(e)

import shutil
@mcp.tool()
def move_file(source:str, destination:str):
    """moves a file """
    src = get_safe_path(source)
    dst = get_safe_path(destination)

    if not src.exists():
        return "file does not exists"
    shutil.move(src, dst)
    return "file move to the destination"


@mcp.tool()
def copy_file(source: str, destination: str):
    """Copy a file."""

    src = get_safe_path(source)
    dst = get_safe_path(destination)

    if not src.exists():
        return "Source file not found."

    shutil.copy2(src, dst)

    return "File copied successfully."


from datetime import datetime

@mcp.tool()
def file_info(path: str):
    """Get information about a file."""

    file_path = get_safe_path(path)

    if not file_path.exists():
        return "File not found."

    stat = file_path.stat()

    return {
        "name": file_path.name,
        "size": stat.st_size,
        "modified": datetime.fromtimestamp(
            stat.st_mtime
        ).isoformat(),
        "is_file": file_path.is_file(),
        "is_directory": file_path.is_dir(),
    }


if __name__ == "__main__":
    mcp.run()
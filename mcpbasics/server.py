from mcp.server.fastmcp import FastMCP

mcp = FastMCP("mcpbasics")

@mcp.tool()
def add(a: int, b: int):
    return a + b

@mcp.tool()
def sub(a:int , b:int):
    return a-b

@mcp.tool()
def mul(a:int, b:int):
    return a*b

@mcp.tool()
def div(a:int, b:int):
    if(b==0):
        return "error not divisble by zero"
    else:
        return a/b

@mcp.tool()
def greet(name: str):
    return f"hello{name}"

@mcp.tool()
def read_file(path: str):
    """Read the contents of a file."""

    with open(path, "r") as file:
        return file.read()
    

@mcp.tool()
def write_file(path: str, content: str):
    """Write content to a file."""

    try:
        with open(path, "w", encoding="utf-8") as file:
            file.write(content)

        return "File written successfully."

    except Exception as e:
        return str(e)

import os

@mcp.tool()
def delete_file(path: str):
    """Delete a file."""

    try:
        os.remove(path)
        return "Deleted successfully."

    except Exception as e:
        return str(e)

if __name__ == "__main__":
    mcp.run()
import asyncio
import os
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    # Resolve the path to server.py relative to this client file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    server_path = os.path.join(current_dir, "server.py")

    server = StdioServerParameters(
        command=sys.executable,  # Uses the currently active python environment/interpreter
        args=[server_path],
    )
    query = input(">>")
    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            result = await session.call_tool(
                "add",
                {
                    "a": 5,
                    "b": 10
                }
            )

            print(result.content[0].text)

            result1 = await session.call_tool(
                "mul",
                {
                    "a": 5,
                    "b": 5
                }
            )

            print(result1.content[0].text)

            output = await session.call_tool(
                "greet",
                {
                    "name": "panshul"
                }
            )

            print(output.content[0].text)

            read = await session.call_tool(
                "read_file",
                {
                    "path":"notes.txt"
                }
            )
            #print(read.content[0].text)

            #write = await session.call_tool(
            #    "write_file",
            #    {
            #        "path":"hello.txt",
            #        "content":"I love this, this is interesting"
            #    }
            #)
            #print(write.content[0].text)

            #await session.call_tool(
            #    "delete_file",
            #   {
            #        "path":"hello.txt"
            #    }
            #)

            tools = await session.list_tools()
            for tools in tools.tools:
                print(tools.name)
                print(tools.description)
                print(tools.inputSchema)

            if query.startswith("read"):
                parts = query.split()
                filename = parts[1]
                result2 = await session.call_tool(
                    "read_file",
                    {
                        "path": filename
                    }
                )
                print(result2.content[0].text)

asyncio.run(main())
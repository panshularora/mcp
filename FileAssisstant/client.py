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

    print("Connecting to FileAssisstant server...")
    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("Connected!")

            # Print available tools
            print("\nAvailable Tools:")
            tools_resp = await session.list_tools()
            for tool in tools_resp.tools:
                print(f"- {tool.name}: {tool.description}")

            print("\nRunning test actions...")

            # 1. List files
            print("\n--- Listing Files ---")
            list_res = await session.call_tool("list_files", {})
            print("Result:", list_res.content[0].text)

            # 2. Write file
            print("\n--- Writing test.txt ---")
            write_res = await session.call_tool(
                "write_file",
                {"path": "test.txt", "content": "Hello from FileAssisstant client!"},
            )
            print("Result:", write_res.content[0].text)

            # 3. List files again
            print("\n--- Listing Files (after write) ---")
            list_res = await session.call_tool("list_files", {})
            print("Result:", list_res.content[0].text)

            # 4. Read file
            print("\n--- Reading test.txt ---")
            read_res = await session.call_tool("read_file", {"path": "test.txt"})
            print("Result:", read_res.content[0].text)

            # 5. Try invalid path (security check)
            print("\n--- Testing Path Traversal Protection ---")
            traversal_res = await session.call_tool(
                "read_file", {"path": "../server.py"}
            )
            print(
                "Result (should be 'Invalid Path'):",
                traversal_res.content[0].text,
            )


if __name__ == "__main__":
    asyncio.run(main())

import asyncio
import os
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


# Resolve the path to server.py relative to this client file
current_dir = os.path.dirname(os.path.abspath(__file__))
server_path = os.path.join(current_dir, "server.py")

server = StdioServerParameters(
    command=sys.executable,  # Uses the currently active python environment/interpreter
    args=[server_path]
)


async def main():
    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:

            await session.initialize()

            print("Connected to GitHub MCP Server\n")

            tools = await session.list_tools()

            while True:

                print("\nAvailable Tools:")
                for tool in tools.tools:
                    print(f"- {tool.name}")

                tool_name = input("\nEnter tool name (or 'exit'): ").strip()

                if tool_name.lower() == "exit":
                    break

                # Find selected tool
                selected_tool = None

                for tool in tools.tools:
                    if tool.name == tool_name:
                        selected_tool = tool
                        break

                if selected_tool is None:
                    print("Tool not found!")
                    continue

                # Build arguments dynamically
                arguments = {}

                schema = selected_tool.inputSchema

                properties = schema.get("properties", {})
                required = schema.get("required", [])

                if properties:
                    print("\nEnter arguments:")

                for name, info in properties.items():

                    field_type = info.get("type", "string")

                    value = input(f"{name} ({field_type}): ")

                    if field_type == "boolean":
                        value = value.lower() in ("true", "1", "yes", "y")

                    elif field_type == "integer":
                        value = int(value)

                    elif field_type == "number":
                        value = float(value)

                    arguments[name] = value

                result = await session.call_tool(
                    tool_name,
                    arguments
                )

                print("\n========== RESULT ==========")
                print(result)
                print("============================\n")


if __name__ == "__main__":
    asyncio.run(main())
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

    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:

            await session.initialize()

            print("✅ Connected to File Assistant MCP Server")

            while True:

                # Fetch all available tools
                tools = await session.list_tools()

                print("\nAvailable Tools:")
                for tool in tools.tools:
                    print(f"- {tool.name}")

                tool_name = input("\nEnter tool name (or 'exit'): ").strip()

                if tool_name.lower() == "exit":
                    print("👋 Goodbye!")
                    break

                # Find the selected tool
                selected_tool = None

                for tool in tools.tools:
                    if tool.name == tool_name:
                        selected_tool = tool
                        break

                if selected_tool is None:
                    print("❌ Tool not found.")
                    continue

                # Show tool info
                print(f"\nTool: {selected_tool.name}")
                print(selected_tool.description)

                # Build arguments dynamically
                schema = selected_tool.inputSchema

                arguments = {}

                properties = schema.get("properties", {})

                if properties:
                    print("\nEnter arguments:")

                for parameter, details in properties.items():

                    parameter_type = details.get("type", "string")

                    value = input(f"{parameter} ({parameter_type}): ")

                    # Convert common primitive types
                    if parameter_type == "integer":
                        value = int(value)

                    elif parameter_type == "number":
                        value = float(value)

                    elif parameter_type == "boolean":
                        value = value.lower() in (
                            "true",
                            "1",
                            "yes",
                            "y",
                        )

                    arguments[parameter] = value

                # Call tool
                try:
                    result = await session.call_tool(
                        selected_tool.name,
                        arguments,
                    )

                    print("\n========== RESULT ==========")
                    print(result)
                    print("============================")

                except Exception as e:
                    print(f"\nError: {e}")


if __name__ == "__main__":
    asyncio.run(main())
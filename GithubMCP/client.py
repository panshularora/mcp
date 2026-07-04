import asyncio
import json
import os
import sys

from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from openai import OpenAI

# Load credentials from .env
load_dotenv()

# Verify required keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

if not OPENAI_API_KEY:
    print("Warning: OPENAI_API_KEY is not set in your .env file.")
if not GITHUB_TOKEN:
    print("Warning: GITHUB_TOKEN is not set in your .env file.")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Resolve path to server.py dynamically
current_dir = os.path.dirname(os.path.abspath(__file__))
server_path = os.path.join(current_dir, "server.py")

# Configure the Stdio parameters for starting the server
server_params = StdioServerParameters(
    command=sys.executable,
    args=[server_path]
)


def mcp_to_openai_tool(mcp_tool):
    """Convert an MCP tool schema to an OpenAI tool definition."""
    schema = mcp_tool.inputSchema
    # Fallback to empty object if schema properties are missing
    if not isinstance(schema, dict):
        schema = {"type": "object", "properties": {}}

    return {
        "type": "function",
        "function": {
            "name": mcp_tool.name,
            "description": mcp_tool.description,
            "parameters": schema
        }
    }


async def run_agent():
    print("Initializing GitHub MCP Server connection...")

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize MCP session
            await session.initialize()
            print("Connected to GitHub MCP Server!")

            # 1. Discover tools dynamically
            tools_resp = await session.list_tools()
            mcp_tools = tools_resp.tools

            # 2. Translate MCP tools to OpenAI specifications
            openai_tools = [mcp_to_openai_tool(t) for t in mcp_tools]

            # System instruction that outlines capabilities
            system_prompt = (
                "You are an expert GitHub AI Agent. You help users manage repositories, "
                "issues, pull requests, and search code using the provided tools. "
                "When you are asked to perform tasks, choose the correct tool(s) dynamically. "
                "If a tool call returns an error or empty result, explain the status clearly. "
                "Be helpful, precise, and summarize code search results concisely."
            )

            messages = [{"role": "system", "content": system_prompt}]

            print("\n===========================================")
            print("   GitHub AI Agent (MCP + OpenAI) Online   ")
            print("===========================================")
            print("Type 'exit' to quit.")

            while True:
                try:
                    user_input = input("\nYou: ").strip()
                except (KeyboardInterrupt, EOFError):
                    print("\nGoodbye!")
                    break

                if not user_input:
                    continue

                if user_input.lower() == "exit":
                    print("Goodbye!")
                    break

                messages.append({"role": "user", "content": user_input})

                # Agent loop (for handling multi-step tool calls and reasoning)
                while True:
                    print("Thinking...")
                    try:
                        response = client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=messages,
                            tools=openai_tools if openai_tools else None,
                            tool_choice="auto" if openai_tools else None
                        )
                    except Exception as ex:
                        print(f"OpenAI API Error: {ex}")
                        break

                    assistant_message = response.choices[0].message
                    tool_calls = assistant_message.tool_calls

                    # If GPT doesn't want to call any tools, output final reply
                    if not tool_calls:
                        messages.append({"role": "assistant", "content": assistant_message.content})
                        print(f"\nAgent: {assistant_message.content}")
                        break

                    # Append tool calls to message history
                    messages.append(assistant_message)

                    # Execute requested tools
                    for tool_call in tool_calls:
                        tool_name = tool_call.function.name
                        tool_args = json.loads(tool_call.function.arguments)

                        print(f"Tool Call -> {tool_name}({json.dumps(tool_args)})")

                        try:
                            # Invoke tool on the MCP server
                            result = await session.call_tool(tool_name, tool_args)

                            # Extract result content
                            if hasattr(result, "content") and result.content:
                                result_text = result.content[0].text
                            else:
                                result_text = str(result)

                        except Exception as e:
                            result_text = f"Error executing tool {tool_name}: {str(e)}"

                        print(f"Tool Output -> {result_text[:150]}...")

                        # Append tool result to messages history
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "name": tool_name,
                            "content": result_text
                        })


if __name__ == "__main__":
    if not OPENAI_API_KEY:
        print("Error: OPENAI_API_KEY environment variable is missing from .env.")
        print("Please configure your OpenAI API Key inside c:/Users/Panshul/Desktop/mcp/GithubMCP/.env to start the agent.")
    else:
        asyncio.run(run_agent())
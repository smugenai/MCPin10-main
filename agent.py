# Import smolagents 
from smolagents import ToolCallingAgent, ToolCollection, LiteLLMModel
# Bring in MCP Client Side libraries
from mcp import StdioServerParameters

# Specify Ollama LLM via LiteLLM
model = LiteLLMModel(
        model_id="ollama_chat/llama3.2",
        num_ctx=8192) 

# Outline STDIO stuff to get to MCP Tools
server_parameters = StdioServerParameters(
    command="python",
    args=["server.py"],
    env=None,
)

# Run the agent using the MCP tools 
with ToolCollection.from_mcp(server_parameters, trust_remote_code=True) as tool_collection:
    agent = ToolCallingAgent(tools=[*tool_collection.tools], model=model)
    agent.run("What was EBITDA for IBM?")

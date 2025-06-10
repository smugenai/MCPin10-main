# Import yahoo finance 
import yfinance as yf
# Bring in colorama for fancy printing
from colorama import Fore
# Bring in MCP Server SDK
from mcp.server.fastmcp import FastMCP


# Create server 
mcp = FastMCP("yfinanceserver")

# Add in a prompt function

                
# Build server function


# Add in a stock info tool 


# Add in an income statement tool
@mcp.tool()


# Kick off server if file is run 
if __name__ == "__main__":
    mcp.run(transport="stdio")

# Import yahoo finance 
import yfinance as yf
# Bring in colorama for fancy printing
from colorama import Fore
# Bring in MCP Server SDK
from mcp.server.fastmcp import FastMCP

# Create server 
mcp = FastMCP("yfinanceserver")

# Add in a prompt function
@mcp.prompt()
def stock_summary(stock_data:str) -> str:
    """Prompt template for summarising stock price"""
    return f"""You are a financial assistant who summarises stock data.
                Using the information below, summarise the data relevant for stock price movement
                Data {stock_data}"""               

# Build server function
@mcp.tool()
def stock_price(stock_ticker: str) -> str:
    """Returns last price for given stock ticker.
    Args:
        stock_ticker:  
        Example payload: "NVDA"

    Returns:
        str:"Ticker: Last Price" 
        Example Respnse "NVDA: $100.21" 
        """
    # Specify stock ticker 
    dat = yf.Ticker(stock_ticker)
    # Get historical prices
    historical_prices = dat.history(period='1mo')
    # Filter on closes only
    last_months_closes = historical_prices['Close']
    print(Fore.YELLOW + str(last_months_closes))
    return str(f"Stock price over the last month for {stock_ticker}: {last_months_closes}")

# Add in a stock info tool 
@mcp.tool()
def stock_info(stock_ticker: str) -> str:
    """Returns information about a stock given its ticker.
    Args:
        stock_ticker
        Example payload: "IBM"

    Returns:
        str:information about company
        """
    dat = yf.Ticker(stock_ticker)
    
    return str(f"Background information for {stock_ticker}: {dat.info}")


# Add in an income statement tool
@mcp.tool()
def income_statement(stock_ticker: str) -> str:
    """This tool returns quarterly income statement for a given stock ticker.
    Args:
        stock_ticker: 
        Example payload: "BOA"

    Returns:
        str:quarterly income statement for the company
        """
    dat = yf.Ticker(stock_ticker)   
    income_stmt = dat.quarterly_income_stmt

    if income_stmt.empty:
        return f"No quarterly income statement found for {stock_ticker}."

    formatted_string = income_stmt.style.format("{:,.0f}", na_rep="-").to_string()

    return str(f"Quarterly income statement for {stock_ticker}:\n{formatted_string}")

# Kick off server if file is run 
if __name__ == "__main__":
    mcp.run(transport="stdio")


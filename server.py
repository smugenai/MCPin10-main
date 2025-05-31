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
    return f"""You are a helpful financial assistant designed to summarise stock data.
                Using the information below, summarise the pertintent points relevant to stock price movement
                Data {stock_data}"""
                
# Add in a resource function
import chromadb
chroma_client = chromadb.PersistentClient(path="ticker_db")
collection = chroma_client.get_collection(name="stock_tickers")
@mcp.resource("tickers://search/{stock_name}")
def list_tickers(stock_name:str)->str: 
    """This resource allows you to find a stock ticker by passing through a stock name e.g. Google, Bank of America etc. 
        It returns the result from a vector search using a similarity metric. 
    Args:
        stock_name: Name of the stock you want to find the ticker for
        Example payload: "Protor and Gamble"

    Returns:
        str:"Ticker: Last Price" 
        Example Respnse 
        {'ids': [['41', '30']], 'embeddings': None, 'documents': [['AZN - ASTRAZENECA PLC', 'NVO - NOVO NORDISK A S']], 'uris': None, 'included': ['metadatas', 'documents', 'distances'], 'data': None, 'metadatas': [[None, None]], 'distances': [[1.1703131198883057, 1.263759970664978]]}
        
    """
    results = collection.query(query_texts=[stock_name], n_results=1) 
    return str(results) 
    
# Build server function
@mcp.tool()
def stock_price(stock_ticker: str) -> str:
    """This tool returns the last known price for a given stock ticker.
    Args:
        stock_ticker: a alphanumeric stock ticker 
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
    """This tool returns information about a given stock given it's ticker.
    Args:
        stock_ticker: a alphanumeric stock ticker
        Example payload: "IBM"

    Returns:
        str:information about the company
        Example Respnse "Background information for IBM: {'address1': 'One New Orchard Road', 'city': 'Armonk', 'state': 'NY', 'zip': '10504', 'country': 'United States', 'phone': '914 499 1900', 'website': 
                'https://www.ibm.com', 'industry': 'Information Technology Services',... }" 
        """
    dat = yf.Ticker(stock_ticker)
    
    return str(f"Background information for {stock_ticker}: {dat.info}")

# Add in an income statement tool
@mcp.tool()
def income_statement(stock_ticker: str) -> str:
    """This tool returns the quarterly income statement for a given stock ticker.
    Args:
        stock_ticker: a alphanumeric stock ticker
        Example payload: "BOA"

    Returns:
        str:quarterly income statement for the company
        Example Respnse "Income statement for BOA: 
        Tax Effect Of Unusual Items                           76923472.474289  ...          NaN
        Tax Rate For Calcs                                            0.11464  ...          NaN
        Normalized EBITDA                                        4172000000.0  ...          NaN
        """

    dat = yf.Ticker(stock_ticker)
    
    
    return str(f"Background information for {stock_ticker} {dat.quarterly_income_stmt}")

# Kick off server if file is run 
if __name__ == "__main__":
    mcp.run(transport="stdio")
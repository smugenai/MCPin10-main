# Custom MCP server and agent

This project demonstrates how to build a Model Context Protocol (MCP) Server for Yahoo Finance data in Python.

## Quick Start

1. Create a virtual environment:
   - On macOS/Linux:
     ```zsh
     python3 -m venv .venv
     source .venv/bin/activate
     ```
   - On Windows (Command Prompt):
     ```cmd
     python -m venv .venv
     .venv\Scripts\activate
     ```
   - On Windows (PowerShell):
     ```powershell
     python -m venv .venv
     .venv\Scripts\Activate.ps1
     ```
2. Install dependencies:
   ```zsh
   pip install -r requirements.txt
   ```
3. Run the MCP inspector:
   ```zsh
   python server.py
   ```
4. Run the agent:
   ```zsh
   python agent.py
   ```


**Note:** Make sure you have Ollama running to access the LLM.

## References
- MCP SDK: https://github.com/modelcontextprotocol/create-python-server

Original files by Nick Renotte, Modified by SMUGENAI

## License
MIT

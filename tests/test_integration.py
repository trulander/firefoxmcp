import asyncio
import pytest
import re
import os
import base64
from fastmcp import Client

MCP_URL = os.getenv("MCP_URL", "http://foxmcp:3000/mcp")

@pytest.fixture
async def mcp_client():
    client = Client(MCP_URL)
    async with client:
        yield client

@pytest.mark.asyncio
async def test_mcp_connection(mcp_client):
    await mcp_client.ping()
    tools = await mcp_client.list_tools()
    assert len(tools) > 0
    print(f"\nMCP connected! Found {len(tools)} tools")

@pytest.mark.asyncio
async def test_full_browser_workflow(mcp_client):
    """Test: create tab -> Google -> search -> verify DOM -> screenshot"""
    
    # 1. Create a new tab
    print("\nCreating new tab...")
    result = await mcp_client.call_tool("tabs_create", {"url": "about:blank", "active": True})
    print(f"Tab creation result: {result}")
    
    # Search for ID flexibly
    match = re.search(r"ID (\d+)", str(result)) or re.search(r"tab (\d+)", str(result)) or re.search(r"(\d+)", str(result))
    assert match, f"Could not get tab_id from creation result: {result}"
    tab_id = int(match.group(1))
    print(f"Using new tab_id: {tab_id}")
    
    # 2. Navigate to Google
    print(f"Navigating to Google...")
    await mcp_client.call_tool("navigation_go_to_url", {"tab_id": tab_id, "url": "https://www.google.com"})
    await asyncio.sleep(12) 
    
    # 3. Enter 'youtube'
    print("Searching for 'youtube'...")
    search_js = """
    (function() {
        const input = document.querySelector('textarea[name="q"]') || 
                     document.querySelector('input[name="q"]');
        if (input) {
            input.value = "youtube";
            const form = input.closest('form');
            if (form) {
                form.submit();
                return "ok";
            }
        }
        return "not_found";
    })()
    """
    res = await mcp_client.call_tool("content_execute_script", {"tab_id": tab_id, "code": search_js})
    print(f"Search JS Result: {res}")
    assert "ok" in str(res)
    await asyncio.sleep(12) 
    
    # 4. Verify DOM
    print("Verifying DOM content...")
    dom_text = await mcp_client.call_tool("content_get_text", {"tab_id": tab_id, "max_length": 5000})
    text_content = str(dom_text).lower()
    assert "youtube" in text_content
    print("Youtube found in search results!")

    # 5. Take screenshot
    print("Capturing screenshot...")
    os.makedirs("/app/tests/output", exist_ok=True)
    screenshot_path = "/app/tests/output/final_verification.png"
    
    result = await mcp_client.call_tool("tabs_capture_screenshot", {})
    res_str = str(result)
    
    if "data:image/png;base64," in res_str:
        start_idx = res_str.find("data:image/png;base64,") + len("data:image/png;base64,")
        b64_part = res_str[start_idx:]
        b64_clean = ""
        for char in b64_part:
            if char.isalnum() or char in "+/=":
                b64_clean += char
            else:
                break
        
        missing_padding = len(b64_clean) % 4
        if missing_padding:
            b64_clean += "=" * (4 - missing_padding)
            
        with open(screenshot_path, "wb") as f:
            f.write(base64.b64decode(b64_clean))
        
        assert os.path.exists(screenshot_path)
        print(f"Screenshot successfully saved to {screenshot_path}")
    else:
        print("Warning: Could not extract screenshot base64")

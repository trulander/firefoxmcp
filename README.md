# FoxMCP: Firefox Automation via Model Context Protocol (MCP)
[![Russian](https://img.shields.io/badge/lang-English-blue)](README.ru.md)

A complete Docker stack for controlling a real Firefox browser through the Model Context Protocol (MCP). It provides full GUI access via noVNC and a robust HTTP endpoint for AI agents.

## Features
- **Real Firefox Browser**: Headful Firefox ESR running in Xvfb.
- **noVNC Access**: Visual access to the browser via web-browser (no password).
- **FoxMCP Extension**: Pre-installed and pre-configured browser extension.
- **MCP HTTP Server**: FastMCP-based server providing 35 tools for browser automation.
- **Integration Tests**: Built-in test suite using Pytest and UV to verify the whole stack.

## Architecture
- **Service: `firefox`**: Runs X11, Firefox, and noVNC.
- **Service: `foxmcp`**: A Python-based server that bridges MCP requests to the Firefox extension via WebSockets.
- **Service: `tester`**: An ephemeral container that runs integration tests. All test-related files (`pyproject.toml`, `uv.lock`, tests) are located in the `tests/` directory.

## Port Mapping
| Port | Service | Purpose |
|------|---------|---------|
| `6080` | `firefox` | noVNC Web GUI (http://localhost:6080) |
| `3000` | `foxmcp` | MCP HTTP endpoint (http://localhost:3000/mcp) |
| `8765` | `foxmcp` | Internal WebSocket port for extension communication |

## Deployment

1. **Start the stack**:
   ```bash
   docker compose up --build -d
   ```

2. **Run Integration Tests**:
   ```bash
   docker compose up --build tester
   ```

## Complete MCP Tools List (35 tools)

### Window Management
- `list_windows`: List all browser windows and their tabs.
- `get_window`: Get info about a specific window.
- `get_current_window`: Get the current active window.
- `get_last_focused_window`: Get the last focused window.
- `create_window`: Create a new browser window (supports size, position, incognito).
- `close_window`: Close a specific window.
- `focus_window`: Bring a window to front and focus it.
- `update_window`: Update window properties (state, size, position).

### Tab Management
- `tabs_list`: List all open browser tabs with status indicators.
- `tabs_create`: Create a new browser tab with a specific URL.
- `tabs_close`: Close a specific tab.
- `tabs_switch`: Switch to a specific browser tab.
- `tabs_capture_screenshot`: Capture a screenshot of the visible tab (base64 or file).

### Navigation
- `navigation_go_to_url`: Navigate a tab to a specific URL.
- `navigation_back`: Navigate back in browser history.
- `navigation_forward`: Navigate forward in browser history.
- `navigation_reload`: Reload a page in a tab (supports cache bypass).

### Content Interaction
- `content_get_text`: Extract all text content from a tab's page.
- `content_get_html`: Get the full HTML source of a page.
- `content_execute_script`: Execute custom JavaScript in a tab.
- `content_execute_predefined`: Execute a predefined external script.

### History & Bookmarks
- `history_query`: Search through browser history with time filters.
- `history_get_recent`: Get recent browser history items.
- `history_delete_item`: Delete a specific history item by URL.
- `bookmarks_list`: List browser bookmarks (folders and items).
- `bookmarks_search`: Search for specific bookmarks.
- `bookmarks_create`: Create a new bookmark.
- `bookmarks_create_folder`: Create a new bookmark folder.
- `bookmarks_update`: Update bookmark title or URL.
- `bookmarks_delete`: Delete a bookmark.

### Network Monitoring
- `requests_start_monitoring`: Start monitoring network requests (JSON/Text) with URL patterns.
- `requests_stop_monitoring`: Stop monitoring with graceful drainage.
- `requests_list_captured`: List captured request summaries.
- `requests_get_content`: Get full request/response body for a specific ID.

### Debugging
- `debug_websocket_status`: Get status information about the extension connection.

## External Resources
- **FoxMCP Extension & Server**: [ThinkerYzu/foxmcp](https://github.com/ThinkerYzu/foxmcp)
- **noVNC**: [novnc/noVNC](https://github.com/novnc/noVNC)
- **websockify**: [novnc/websockify](https://github.com/novnc/websockify)

## Usage in Claude/Cursor
Add the following to your MCP configuration:
```json
{
  "mcpServers": {
    "firefox": {
      "type": "http",
      "url": "http://localhost:3000/mcp"
    }
  }
}
```

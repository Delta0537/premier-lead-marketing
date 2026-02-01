# 🚀 How to Start Claude & Gemini MCP Servers

## ✅ AUTOMATIC (Recommended)

**They start automatically when Cursor starts!**

1. **Cursor reads your MCP config:** `C:\Users\dezel\.cursor\mcp.json`
2. **Both MCP servers start automatically** when Cursor opens
3. **No manual action needed** - just restart Cursor if they're not working

---

## 🔍 How to Verify They're Running

### **Method 1: Check Cursor Logs**
1. Open Cursor
2. Go to **View → Output** (or `Ctrl+Shift+U`)
3. Look for MCP-related messages:
   - "MCP server started: claude"
   - "MCP server started: gemini"

### **Method 2: Check MCP Status**
1. Open Cursor Command Palette (`Ctrl+Shift+P`)
2. Search for "MCP" commands
3. Look for MCP-related options (should show Claude and Gemini)

### **Method 3: Restart Cursor**
If you're not sure they're running:
1. **Completely close Cursor** (not just the window, quit the app)
2. **Restart Cursor**
3. MCP servers should start automatically on launch

---

## 🔧 MANUAL START (If Automatic Doesn't Work)

### **Option 1: Start Both in Separate Terminals**

**Terminal 1 (Claude):**
```powershell
$env:ANTHROPIC_API_KEY='YOUR_ANTHROPIC_API_KEY_HERE'
npx -y @anthropic-ai/claude-mcp
```

**Terminal 2 (Gemini):**
```powershell
$env:GEMINI_API_KEY='YOUR_GEMINI_API_KEY_HERE'
npx -y gemini-mcp --model gemini-1.5-flash
```

### **Option 2: PowerShell Script (Start Both Together)**

Create a file `start_mcp_servers.ps1`:
```powershell
# Start Claude MCP
Start-Process powershell -ArgumentList "-NoExit", "-Command", "`$env:ANTHROPIC_API_KEY='YOUR_ANTHROPIC_API_KEY_HERE'; npx -y @anthropic-ai/claude-mcp"

# Start Gemini MCP
Start-Process powershell -ArgumentList "-NoExit", "-Command", "`$env:GEMINI_API_KEY='YOUR_GEMINI_API_KEY_HERE'; npx -y gemini-mcp --model gemini-1.5-flash"

Write-Host "MCP servers starting in separate windows..."
```

Run it:
```powershell
.\start_mcp_servers.ps1
```

---

## 📋 Your Current MCP Config

**File:** `C:\Users\dezel\.cursor\mcp.json`

```json
{
  "mcpServers": {
    "gemini": {
      "command": "npx",
      "args": ["-y", "gemini-mcp", "--model", "gemini-1.5-flash"],
      "env": {
        "GEMINI_API_KEY": "YOUR_GEMINI_API_KEY_HERE"
      }
    },
    "claude": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/claude-mcp"],
      "env": {
        "ANTHROPIC_API_KEY": "YOUR_ANTHROPIC_API_KEY_HERE"
      }
    }
  }
}
```

**Both are configured!** Cursor should start them automatically.

---

## ⚠️ Troubleshooting

### **If MCP servers don't start automatically:**

1. **Check MCP config file exists:**
   ```powershell
   Test-Path "C:\Users\dezel\.cursor\mcp.json"
   ```

2. **Verify API keys are correct** in the config file

3. **Check Cursor version** - MCP support requires recent Cursor version

4. **Restart Cursor completely** (quit and reopen)

5. **Check Cursor logs** for errors:
   - View → Output → Look for "MCP" errors

### **If you get 404 errors:**

- **Gemini:** Model name might be wrong - try `gemini-2.0-flash-lite` instead of `gemini-1.5-flash`
- **Claude:** Check API key is valid and has credits
- **Both:** Check API quotas haven't been exceeded

---

## 💡 Best Practice

**Just restart Cursor** - it should handle everything automatically via the `mcp.json` config file. Manual starting is usually only needed for troubleshooting.

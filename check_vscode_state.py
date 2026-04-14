import sqlite3

db = r'C:\Users\DUC CANH PC\AppData\Roaming\Code\User\workspaceStorage\2f1a411419f00f4e894fffc865f7d182\state.vscdb'
conn = sqlite3.connect(db)

# Xoa het cache MCP
conn.execute("DELETE FROM ItemTable WHERE key IN ('mcpToolCache', 'mcpInputs', 'mcp.extCachedServers')")
conn.commit()
print("Deleted MCP cache entries")

# Verify
rows = conn.execute("SELECT key FROM ItemTable WHERE key LIKE '%mcp%'").fetchall()
print("Remaining mcp keys:", rows)
conn.close()




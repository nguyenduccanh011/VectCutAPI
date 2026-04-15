import sqlite3

db = r'C:\Users\DUC CANH PC\AppData\Roaming\Code\User\workspaceStorage\2f1a411419f00f4e894fffc865f7d182\state.vscdb'
conn = sqlite3.connect(db)

keys = ['mcpToolCache', 'mcpInputs', 'mcp.extCachedServers']
for k in keys:
    conn.execute("DELETE FROM ItemTable WHERE key=?", (k,))
    print(f"Deleted: {k}")

conn.commit()
conn.close()
print("Done.")

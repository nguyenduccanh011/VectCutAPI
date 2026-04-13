# MCP Server Configuration Guide

## Vấn đề
Khi phát triển trên nhiều máy khác nhau, lệnh Python có thể khác nhau:
- Một số máy có `python3` 
- Một số máy có `python`
- Đường dẫn tuyệt đối sẽ khác nhau trên mỗi máy

## Giải pháp

Dự án đã cấu hình các script launcher tự động tìm Python khả dụng:

### 🪟 Windows
- Sử dụng file: `.vscode/mcp.json` (đặt sẵn)
- Script launcher: `.vscode/run-mcp.cmd`
- Script này tự động detect `python3` hoặc `python`

```json
{
  "servers": {
    "capcut-api": {
      "type": "stdio",
      "command": ".vscode/run-mcp.cmd",
      "cwd": "${workspaceFolder}",
      "env": {
        "PYTHONPATH": "${workspaceFolder}"
      }
    }
  }
}
```

### 🍎 macOS / 🐧 Linux
- Sử dụng file: `.vscode/mcp.json.macos`
- Script launcher: `.vscode/run-mcp.sh`

**Cách setup:**
```bash
# Copy phiên bản macOS
cp .vscode/mcp.json.macos .vscode/mcp.json

# Đảm bảo script có quyền execute
chmod +x .vscode/run-mcp.sh
```

### Các file cần biết

| File | Mục đích | 
|------|---------|
| `.vscode/mcp.json` | Cấu hình hiện tại (Windows) |
| `.vscode/mcp.json.macos` | Template cho macOS/Linux |
| `.vscode/run-mcp.cmd` | Launcher cho Windows |
| `.vscode/run-mcp.sh` | Launcher cho macOS/Linux |
| `.vscode/launcher.py` | Python wrapper (tùy chọn) |

## Cách hoạt động

### Script Launcher Windows (run-mcp.cmd)
```batch
@echo off
REM Tìm python3 hoặc python
for /f %%i in ('where python3 2>nul') do set PYTHON=%%i
if not defined PYTHON (
    for /f %%i in ('where python 2>nul') do set PYTHON=%%i
)
%PYTHON% mcp_server.py
```

### Script Launcher Unix (run-mcp.sh)
```bash
#!/bin/bash
# Tìm python3 hoặc python
if command -v python3 &> /dev/null; then
    python3 mcp_server.py
elif command -v python &> /dev/null; then
    python mcp_server.py
else
    echo "Error: Python not found"
    exit 1
fi
```

## Troubleshooting

### ❌ Lỗi: "spawn python ENOENT"
- Windows: Chỉnh sửa `.vscode/mcp.json` để sử dụng `run-mcp.cmd`
- macOS/Linux: Copy `.vscode/mcp.json.macos` sang `.vscode/mcp.json` và chạy `chmod +x .vscode/run-mcp.sh`

### ❌ Lỗi: "Permission denied" trên Unix
```bash
chmod +x .vscode/run-mcp.sh
```

### ✅ Kiểm tra Python khả dụng
```powershell
# Windows
where python
where python3

# macOS/Linux
which python
which python3
```

## Cách commit lên Git

**Luôn commit tất cả file:**
```bash
git add .vscode/*.cmd
git add .vscode/*.sh
git add .vscode/mcp.json*
git add .vscode/launcher.py
```

**Mỗi máy tùy chọn OS và copy file phù hợp:**
1. Windows: giữ `.vscode/mcp.json` như hiện tại
2. macOS/Linux: `cp .vscode/mcp.json.macos .vscode/mcp.json`

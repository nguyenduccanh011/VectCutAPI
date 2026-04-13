# VectCutAPI - AI-Powered Video Editing Made Easy   [Try Online](https://www.vectcut.com)

## Project Overview

[VectCut](https://www.vectcut.com) is a **toA (toAgent)** video editing tool. It provides rich cloud-based editing APIs, Skills (including features like subtitles, illustrations, picture-in-picture, AI dubbing, filters, and more).

You can use our editing tools in any Agent platform, whether it's human-orchestrated workflow platforms (such as **Coze, Dify, N8N**) or autonomous planning platforms (such as **OpenClaw, Claude Code, Trae**). This enables you to automatically and batch-produce videos.

We have open-sourced the interface code on GitHub to help various AI tools learn our API. Instead of fine-tuning models ourselves, we let AI actively learn our interfaces (interested? Give us a star so AI picks it up faster 🤩).


### Core Advantages

1. Provide powerful editing capabilities through API methods

2. Real-time preview of editing results on the web without downloading, greatly facilitating workflow development

3. Download editing results and import them into CapCut for secondary editing

4. Use API to generate videos from editing results, achieving full cloud-based operations

## Demo Videos

<div align="center">

**MCP: Create Your Own Video Editing Agent**

[![AI Cut](https://img.youtube.com/vi/fBqy6WFC78E/hqdefault.jpg)](https://www.youtube.com/watch?v=fBqy6WFC78E)

**Combine AI-Generated Images and Videos with VectCutAPI**

[![Airbnb](https://img.youtube.com/vi/1zmQWt13Dx0/hqdefault.jpg)](https://www.youtube.com/watch?v=1zmQWt13Dx0)

[![Horse](https://img.youtube.com/vi/IF1RDFGOtEU/hqdefault.jpg)](https://www.youtube.com/watch?v=IF1RDFGOtEU)

[![Song](https://img.youtube.com/vi/rGNLE_slAJ8/hqdefault.jpg)](https://www.youtube.com/watch?v=rGNLE_slAJ8)

</div>

## Core Features

| Feature Module | API | MCP Protocol | Description |
|---------|----------|----------|------|
| **Draft Management** | ✅ | ✅ | Create, save CapCut draft files |
| **Video Processing** | ✅ | ✅ | Multi-format video import, editing, transitions, effects |
| **Audio Editing** | ✅ | ✅ | Audio tracks, volume control, sound effects |
| **Image Processing** | ✅ | ✅ | Image import, animations, masks, filters |
| **Text Editing** | ✅ | ✅ | Diverse text styles, shadows, backgrounds, animations |
| **Subtitle System** | ✅ | ✅ | SRT subtitle import, style settings, time sync |
| **Effect Engine** | ✅ | ✅ | Visual effects, filters, transition animations |
| **Sticker System** | ✅ | ✅ | Sticker materials, position control, animation effects |
| **Keyframes** | ✅ | ✅ | Property animations, timeline control, easing functions |
| **Media Analysis** | ✅ | ✅ | Video duration detection, format detection |

## Quick Start

### 1. System Requirements

- Python 3.10+
- CapCut or CapCut International Version
- FFmpeg

### 2. Installation & Deployment

```bash
# 1. Clone the project
git clone https://github.com/sun-guannan/VectCutAPI.git
cd VectCutAPI

# 2. Create virtual environment (recommended)
python -m venv venv-capcut
source venv-capcut/bin/activate  # Linux/macOS
# or venv-capcut\Scripts\activate  # Windows

# 3. Install dependencies
pip install -r requirements.txt      # HTTP API basic dependencies
pip install -r requirements-mcp.txt  # MCP protocol support (optional)

# 4. Configuration
cp config.json.example config.json
# Edit config.json as needed
```

### 3. Start Service

```bash
python capcut_server.py # Start HTTP API server, default port: 9001

python mcp_server.py # Start MCP protocol server, supports stdio communication
```

## MCP Integration Guide

[MCP Documentation](./MCP_Documentation_English.md) • [MCP 中文文档](./MCP_文档_中文.md)

### 1. Client Configuration

Create or update `mcp_config.json` configuration file:

```json
{
  "mcpServers": {
    "capcut-api": {
      "command": "python3",
      "args": ["mcp_server.py"],
      "cwd": "/path/to/CapCutAPI",
      "env": {
        "PYTHONPATH": "/path/to/CapCutAPI",
        "DEBUG": "0"
      }
    }
  }
}
```

### 2. Connection Testing

```bash
# Test MCP connection
python test_mcp_client.py

# Expected output
✅ MCP server started successfully
✅ Retrieved 11 available tools
✅ Draft creation test passed
```

## Usage Examples

### 1. API Examples

Add video content:

```python
import requests

# Add background video
response = requests.post("http://localhost:9001/add_video", json={
    "video_url": "https://example.com/background.mp4",
    "start": 0,
    "end": 10,
    "volume": 0.8,
    "transition": "fade_in"
})

print(f"Video added: {response.json()}")
```

Create styled text:

```python
import requests

# Add title text
response = requests.post("http://localhost:9001/add_text", json={
    "text": "Welcome to CapCutAPI",
    "start": 0,
    "end": 5,
    "font": "Noto Sans",
    "font_color": "#FFD700",
    "font_size": 48,
    "shadow_enabled": True,
    "background_color": "#000000"
})

print(f"Text added: {response.json()}")
```

Find more examples in `example.py`.

### 2. MCP Protocol Examples

Complete workflow:

```python
# 1. Create new project
draft = mcp_client.call_tool("create_draft", {
    "width": 1080,
    "height": 1920
})
draft_id = draft["result"]["draft_id"]

# 2. Add background video
mcp_client.call_tool("add_video", {
    "video_url": "https://example.com/bg.mp4",
    "draft_id": draft_id,
    "start": 0,
    "end": 10,
    "volume": 0.6
})

# 3. Add title text
mcp_client.call_tool("add_text", {
    "text": "AI-Powered Video Production",
    "draft_id": draft_id,
    "start": 1,
    "end": 6,
    "font_size": 56,
    "shadow_enabled": True,
    "background_color": "#1E1E1E"
})

# 4. Save project
mcp_client.call_tool("save_draft", {
    "draft_id": draft_id
})
```

## Project Structure

```
VectCutAPI/
├── capcut_server.py           # HTTP API server
├── mcp_server.py              # MCP protocol server
├── config.json                # Configuration file
├── requirements.txt           # HTTP API dependencies
├── requirements-mcp.txt       # MCP dependencies
├── pyJianYingDraft/           # CapCut draft processing
│   ├── segment.py             # Base segment class
│   ├── video_segment.py       # Video segment
│   ├── audio_segment.py       # Audio segment
│   ├── text_segment.py        # Text segment
│   └── ...
├── vectcut-skill/             # Claude Code Skill
│   ├── skill/SKILL.md         # Skill metadata
│   ├── skill/scripts/         # Python client
│   └── skill/references/      # API reference
├── template/                  # Video templates
├── examples/                  # Example code
└── docs/                      # Documentation
```

## Available Tools (MCP Protocol)

| Tool | Function | Main Parameters |
|------|----------|------------------|
| `create_draft` | Create new video draft | width, height |
| `add_text` | Add text element | text, font_size, color, shadow, background |
| `add_video` | Add video track | video_url, start, end, transform, volume |
| `add_audio` | Add audio track | audio_url, volume, speed, effects |
| `add_image` | Add image material | image_url, transform, animation, transition |
| `add_subtitle` | Add subtitle file | srt_path, font_style, position |
| `add_effect` | Add visual effect | effect_type, parameters, duration |
| `add_sticker` | Add sticker element | resource_id, position, scale, rotation |
| `add_video_keyframe` | Add keyframe animation | property_types, times, values |
| `get_video_duration` | Get video duration | video_url |
| `save_draft` | Save draft project | draft_id |

## Configuration Guide

### 1. Basic Configuration

Edit `config.json`:

```json
{
  "capcut_path": "/path/to/CapCut",
  "ffmpeg_path": "/path/to/ffmpeg",
  "api_port": 9001,
  "enable_mcp": true,
  "max_workers": 4
}
```

### 2. Template Configuration

Edit `settings/local.py` to customize:
- Default video resolution
- Default font
- Default effect styles
- Path configurations

## Development Guide

### Running Tests

```bash
# Test HTTP API
python test_flow.py

# Test MCP server
python test_mcp_client.py

# Test specific feature
python -m pytest tests/ -v
```

### Adding New Features

1. Create implementation file: `add_feature_impl.py`
2. Add API endpoint in `capcut_server.py`
3. Add MCP tool in `mcp_server.py`
4. Write tests in `tests/`

## API Server Health Check

```bash
# Check if server is running
curl http://localhost:9001/health

# Expected response
{"status": "ok", "version": "1.0.0"}
```

## Troubleshooting

### Common Issues

**Issue**: Port 9001 already in use
```bash
# Change port in config.json
# or kill existing process
lsof -ti:9001 | xargs kill -9
```

**Issue**: CapCut module not found
```bash
# Install CapCut or set correct path in config.json
# Verify path with:
python -c "import jianying_draft; print('OK')"
```

**Issue**: FFmpeg not found
```bash
# Install FFmpeg
# macOS: brew install ffmpeg
# Windows: Download from https://ffmpeg.org
# Linux: sudo apt-get install ffmpeg
```

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

- 📖 [Documentation](./docs/)
- 🐛 [Issue Tracker](https://github.com/sun-guannan/VectCutAPI/issues)
- 💬 [Discussions](https://github.com/sun-guannan/VectCutAPI/discussions)

## Acknowledgments

- Built with Python, CapCut, and FFmpeg
- Special thanks to all contributors and users

---

**Latest Update**: April 2026 • **Version**: 1.0.0

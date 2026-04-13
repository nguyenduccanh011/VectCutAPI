#!/usr/bin/env python3
"""
CapCut API MCP Server (Complete Version)
"""

import sys
import os
import json
import traceback
import io
import contextlib
from typing import Any, Dict, List, Optional
from i18n import t

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import CapCut API features
try:
    from create_draft import get_or_create_draft
    from add_text_impl import add_text_impl
    from add_video_track import add_video_track
    from add_audio_track import add_audio_track
    from add_image_impl import add_image_impl
    from add_subtitle_impl import add_subtitle_impl
    from add_effect_impl import add_effect_impl
    from add_sticker_impl import add_sticker_impl
    from add_video_keyframe_impl import add_video_keyframe_impl
    from get_duration_impl import get_video_duration
    from save_draft_impl import save_draft_impl
    from pyJianYingDraft.text_segment import TextStyleRange
    CAPCUT_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import CapCut modules: {e}", file=sys.stderr)
    CAPCUT_AVAILABLE = False

# Tool definitions
TOOLS = [
    {
        "name": "create_draft",
        "description": "Create a new CapCut draft",
        "inputSchema": {
            "type": "object",
            "properties": {
                "width": {"type": "integer", "default": 1080, "description": "Video width"},
                "height": {"type": "integer", "default": 1920, "description": "Video height"}
            }
        }
    },
    {
        "name": "add_video",
        "description": "Add a video to draft with transition/mask/background blur support",
        "inputSchema": {
            "type": "object",
            "properties": {
                "video_url": {"type": "string", "description": "Video URL"},
                "draft_id": {"type": "string", "description": "Draft ID"},
                "start": {"type": "number", "default": 0, "description": "Start time (seconds)"},
                "end": {"type": "number", "description": "End time (seconds)"},
                "target_start": {"type": "number", "default": 0, "description": "Target start time (seconds)"},
                "width": {"type": "integer", "default": 1080, "description": "Video width"},
                "height": {"type": "integer", "default": 1920, "description": "Video height"},
                "transform_x": {"type": "number", "default": 0, "description": "X position"},
                "transform_y": {"type": "number", "default": 0, "description": "Y position"},
                "scale_x": {"type": "number", "default": 1, "description": "X scale"},
                "scale_y": {"type": "number", "default": 1, "description": "Y scale"},
                "speed": {"type": "number", "default": 1.0, "description": "Playback speed"},
                "track_name": {"type": "string", "default": "main", "description": "Track name"},
                "volume": {"type": "number", "default": 1.0, "description": "Volume"},
                "transition": {"type": "string", "description": "Transition type"},
                "transition_duration": {"type": "number", "default": 0.5, "description": "Transition duration"},
                "mask_type": {"type": "string", "description": "Mask type"},
                "background_blur": {"type": "integer", "description": "Background blur level (1-4)"}
            },
            "required": ["video_url"]
        }
    },
    {
        "name": "add_audio",
        "description": "Add audio to draft with audio effect support",
        "inputSchema": {
            "type": "object",
            "properties": {
                "audio_url": {"type": "string", "description": "Audio URL"},
                "draft_id": {"type": "string", "description": "Draft ID"},
                "start": {"type": "number", "default": 0, "description": "Start time (seconds)"},
                "end": {"type": "number", "description": "End time (seconds)"},
                "target_start": {"type": "number", "default": 0, "description": "Target start time (seconds)"},
                "volume": {"type": "number", "default": 1.0, "description": "Volume"},
                "speed": {"type": "number", "default": 1.0, "description": "Playback speed"},
                "track_name": {"type": "string", "default": "audio_main", "description": "Track name"},
                "width": {"type": "integer", "default": 1080, "description": "Video width"},
                "height": {"type": "integer", "default": 1920, "description": "Video height"}
            },
            "required": ["audio_url"]
        }
    },
    {
        "name": "add_image",
        "description": "Add image to draft with animation/transition/mask support",
        "inputSchema": {
            "type": "object",
            "properties": {
                "image_url": {"type": "string", "description": "Image URL"},
                "draft_id": {"type": "string", "description": "Draft ID"},
                "start": {"type": "number", "default": 0, "description": "Start time (seconds)"},
                "end": {"type": "number", "default": 3.0, "description": "End time (seconds)"},
                "width": {"type": "integer", "default": 1080, "description": "Video width"},
                "height": {"type": "integer", "default": 1920, "description": "Video height"},
                "transform_x": {"type": "number", "default": 0, "description": "X position"},
                "transform_y": {"type": "number", "default": 0, "description": "Y position"},
                "scale_x": {"type": "number", "default": 1, "description": "X scale"},
                "scale_y": {"type": "number", "default": 1, "description": "Y scale"},
                "track_name": {"type": "string", "default": "main", "description": "Track name"},
                "intro_animation": {"type": "string", "description": "Intro animation"},
                "outro_animation": {"type": "string", "description": "Outro animation"},
                "transition": {"type": "string", "description": "Transition type"},
                "mask_type": {"type": "string", "description": "Mask type"}
            },
            "required": ["image_url"]
        }
    },
    {
        "name": "add_text",
        "description": "Add text to draft with multi-style text, shadow, and background",
        "inputSchema": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "Text content"},
                "start": {"type": "number", "description": "Start time (seconds)"},
                "end": {"type": "number", "description": "End time (seconds)"},
                "draft_id": {"type": "string", "description": "Draft ID"},
                "font_color": {"type": "string", "default": "#ffffff", "description": "Font color"},
                "font_size": {"type": "integer", "default": 24, "description": "Font size"},
                "shadow_enabled": {"type": "boolean", "default": False, "description": "Enable text shadow"},
                "shadow_color": {"type": "string", "default": "#000000", "description": "Shadow color"},
                "shadow_alpha": {"type": "number", "default": 0.8, "description": "Shadow alpha"},
                "shadow_angle": {"type": "number", "default": 315.0, "description": "Shadow angle"},
                "shadow_distance": {"type": "number", "default": 5.0, "description": "Shadow distance"},
                "shadow_smoothing": {"type": "number", "default": 0.0, "description": "Shadow smoothing"},
                "background_color": {"type": "string", "description": "Background color"},
                "background_alpha": {"type": "number", "default": 1.0, "description": "Background alpha"},
                "background_style": {"type": "integer", "default": 0, "description": "Background style"},
                "background_round_radius": {"type": "number", "default": 0.0, "description": "Background corner radius"},
                "text_styles": {"type": "array", "description": "Text style ranges"}
            },
            "required": ["text", "start", "end"]
        }
    },
    {
        "name": "add_subtitle",
        "description": "Add subtitles to draft with SRT and style options",
        "inputSchema": {
            "type": "object",
            "properties": {
                "srt_path": {"type": "string", "description": "SRT file path or URL"},
                "draft_id": {"type": "string", "description": "Draft ID"},
                "track_name": {"type": "string", "default": "subtitle", "description": "Track name"},
                "time_offset": {"type": "number", "default": 0, "description": "Time offset (seconds)"},
                "font": {"type": "string", "description": "Font"},
                "font_size": {"type": "number", "default": 8.0, "description": "Font size"},
                "font_color": {"type": "string", "default": "#FFFFFF", "description": "Font color"},
                "bold": {"type": "boolean", "default": False, "description": "Bold"},
                "italic": {"type": "boolean", "default": False, "description": "Italic"},
                "underline": {"type": "boolean", "default": False, "description": "Underline"},
                "border_width": {"type": "number", "default": 0.0, "description": "Border width"},
                "border_color": {"type": "string", "default": "#000000", "description": "Border color"},
                "background_color": {"type": "string", "default": "#000000", "description": "Background color"},
                "background_alpha": {"type": "number", "default": 0.0, "description": "Background alpha"},
                "transform_x": {"type": "number", "default": 0.0, "description": "X position"},
                "transform_y": {"type": "number", "default": -0.8, "description": "Y position"},
                "width": {"type": "integer", "default": 1080, "description": "Video width"},
                "height": {"type": "integer", "default": 1920, "description": "Video height"}
            },
            "required": ["srt_path"]
        }
    },
    {
        "name": "add_effect",
        "description": "Add an effect to draft",
        "inputSchema": {
            "type": "object",
            "properties": {
                "effect_type": {"type": "string", "description": "Effect type name"},
                "draft_id": {"type": "string", "description": "Draft ID"},
                "start": {"type": "number", "default": 0, "description": "Start time (seconds)"},
                "end": {"type": "number", "default": 3.0, "description": "End time (seconds)"},
                "track_name": {"type": "string", "default": "effect_01", "description": "Track name"},
                "params": {"type": "array", "description": "Effect parameter list"},
                "width": {"type": "integer", "default": 1080, "description": "Video width"},
                "height": {"type": "integer", "default": 1920, "description": "Video height"}
            },
            "required": ["effect_type"]
        }
    },
    {
        "name": "add_sticker",
        "description": "Add a sticker to draft",
        "inputSchema": {
            "type": "object",
            "properties": {
                "resource_id": {"type": "string", "description": "Sticker resource ID"},
                "draft_id": {"type": "string", "description": "Draft ID"},
                "start": {"type": "number", "description": "Start time (seconds)"},
                "end": {"type": "number", "description": "End time (seconds)"},
                "transform_x": {"type": "number", "default": 0, "description": "X position"},
                "transform_y": {"type": "number", "default": 0, "description": "Y position"},
                "scale_x": {"type": "number", "default": 1.0, "description": "X scale"},
                "scale_y": {"type": "number", "default": 1.0, "description": "Y scale"},
                "alpha": {"type": "number", "default": 1.0, "description": "Opacity"},
                "rotation": {"type": "number", "default": 0.0, "description": "Rotation"},
                "track_name": {"type": "string", "default": "sticker_main", "description": "Track name"},
                "width": {"type": "integer", "default": 1080, "description": "Video width"},
                "height": {"type": "integer", "default": 1920, "description": "Video height"}
            },
            "required": ["resource_id", "start", "end"]
        }
    },
    {
        "name": "add_video_keyframe",
        "description": "Add video keyframes for position/scale/rotation/alpha animations",
        "inputSchema": {
            "type": "object",
            "properties": {
                "draft_id": {"type": "string", "description": "Draft ID"},
                "track_name": {"type": "string", "default": "main", "description": "Track name"},
                "property_type": {"type": "string", "description": "Keyframe property type(position_x, position_y, rotation, scale_x, scale_y, uniform_scale, alpha, saturation, contrast, brightness, volume)"},
                "time": {"type": "number", "default": 0.0, "description": "Keyframe time (seconds)"},
                "value": {"type": "string", "description": "Keyframe value"},
                "property_types": {"type": "array", "description": "Batch mode: keyframe property type list"},
                "times": {"type": "array", "description": "Batch mode: keyframe times"},
                "values": {"type": "array", "description": "Batch mode: keyframe value list"}
            }
        }
    },
    {
        "name": "get_video_duration",
        "description": "Get video duration",
        "inputSchema": {
            "type": "object",
            "properties": {
                "video_url": {"type": "string", "description": "Video URL"}
            },
            "required": ["video_url"]
        }
    },
    {
        "name": "save_draft",
        "description": "Save draft",
        "inputSchema": {
            "type": "object",
            "properties": {
                "draft_id": {"type": "string", "description": "Draft ID"}
            }
        }
    }
]

@contextlib.contextmanager
def capture_stdout():
    """Capture stdout to prevent debug logs from breaking JSON responses."""
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        yield sys.stdout
    finally:
        sys.stdout = old_stdout

def convert_text_styles(text_styles_data):
    """Convert dict-style text_styles to a list of TextStyleRange objects."""
    if not text_styles_data:
        return None
    
    try:
        text_style_ranges = []
        for style_dict in text_styles_data:
            style_range = TextStyleRange(
                start=style_dict.get("start", 0),
                end=style_dict.get("end", 0),
                font_size=style_dict.get("font_size"),
                font_color=style_dict.get("font_color"),
                bold=style_dict.get("bold", False),
                italic=style_dict.get("italic", False),
                underline=style_dict.get("underline", False)
            )
            text_style_ranges.append(style_range)
        return text_style_ranges
    except Exception as e:
        print(f"[ERROR] {t('text_styles_conversion_error', error=str(e))}", file=sys.stderr)
        return None

def execute_tool(tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Execute one tool call."""
    try:
        print(f"[DEBUG] Executing tool: {tool_name} with args: {arguments}", file=sys.stderr)
        
        if not CAPCUT_AVAILABLE:
            return {"success": False, "error": t("capcut_modules_unavailable")}
        
        # Capture stdout to avoid mixing debug output with JSON response.
        with capture_stdout() as captured:
            if tool_name == "create_draft":
                draft_id, script = get_or_create_draft(
                    width=arguments.get("width", 1080),
                    height=arguments.get("height", 1920)
                )
                result = {
                    "draft_id": str(draft_id),
                    "draft_url": f"https://www.install-ai-guider.top/draft/downloader?draft_id={draft_id}"
                }
                
            elif tool_name == "add_video":
                result = add_video_track(**arguments)
                
            elif tool_name == "add_audio":
                result = add_audio_track(**arguments)
                
            elif tool_name == "add_image":
                result = add_image_impl(**arguments)
                
            elif tool_name == "add_text":
                # Convert text_styles payload if provided.
                text_styles_converted = None
                if "text_styles" in arguments and arguments["text_styles"]:
                    text_styles_converted = convert_text_styles(arguments["text_styles"])
                    arguments["text_styles"] = text_styles_converted
                
                result = add_text_impl(**arguments)
                
            elif tool_name == "add_subtitle":
                result = add_subtitle_impl(**arguments)
                
            elif tool_name == "add_effect":
                result = add_effect_impl(**arguments)
                
            elif tool_name == "add_sticker":
                result = add_sticker_impl(**arguments)
                
            elif tool_name == "add_video_keyframe":
                result = add_video_keyframe_impl(**arguments)
                
            elif tool_name == "get_video_duration":
                duration = get_video_duration(arguments["video_url"])
                result = {"duration": duration}
                
            elif tool_name == "save_draft":
                save_result = save_draft_impl(**arguments)
                if isinstance(save_result, dict) and "draft_url" in save_result:
                    result = {"draft_url": save_result["draft_url"]}
                else:
                    result = {"draft_url": f"https://www.install-ai-guider.top/draft/downloader?draft_id=unknown"}
                
            else:
                return {"success": False, "error": t("unknown_tool", tool_name=tool_name)}
        
        return {
            "success": True,
            "result": result,
            "features_used": {
                "shadow": arguments.get("shadow_enabled", False) if tool_name == "add_text" else False,
                "background": bool(arguments.get("background_color")) if tool_name == "add_text" else False,
                "multi_style": bool(arguments.get("text_styles")) if tool_name == "add_text" else False
            }
        }
        
    except Exception as e:
        print(f"[ERROR] {t('tool_execution_error', error=str(e))}", file=sys.stderr)
        print(f"[ERROR] Traceback: {traceback.format_exc()}", file=sys.stderr)
        return {"success": False, "error": str(e)}

def handle_request(request_data: str) -> Optional[str]:
    """Handle one JSON-RPC request."""
    try:
        request = json.loads(request_data.strip())
        print(f"[DEBUG] Received request: {request.get('method', 'unknown')}", file=sys.stderr)
        
        if request.get("method") == "initialize":
            response = {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "experimental": {},
                        "tools": {"listChanged": False}
                    },
                    "serverInfo": {
                        "name": "capcut-api",
                        "version": "1.12.3"
                    }
                }
            }
            return json.dumps(response)
            
        elif request.get("method") == "notifications/initialized":
            return None
            
        elif request.get("method") == "tools/list":
            response = {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "result": {"tools": TOOLS}
            }
            return json.dumps(response)
            
        elif request.get("method") == "tools/call":
            tool_name = request["params"]["name"]
            arguments = request["params"].get("arguments", {})
            
            result = execute_tool(tool_name, arguments)
            
            response = {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(result, ensure_ascii=False, indent=2)
                        }
                    ]
                }
            }
            return json.dumps(response)
            
        else:
            error_response = {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "error": {"code": -32601, "message": t("method_not_found")}
            }
            return json.dumps(error_response)
            
    except Exception as e:
        print(f"[ERROR] {t('request_handling_error', error=str(e))}", file=sys.stderr)
        print(f"[ERROR] Traceback: {traceback.format_exc()}", file=sys.stderr)
        error_response = {
            "jsonrpc": "2.0",
            "id": None,
            "error": {"code": 0, "message": str(e)}
        }
        return json.dumps(error_response)

def main():
    """Main entry point."""
    print(f"🚀 {t('starting_server')}", file=sys.stderr)
    print(f"📋 {t('available_tools', count=len(TOOLS))}", file=sys.stderr)
    print(f"✨ {t('feature_summary')}", file=sys.stderr)
    print(f"🔌 {t('waiting_connections')}", file=sys.stderr)
    
    try:
        while True:
            try:
                line = sys.stdin.readline()
                if not line:
                    print(f"[DEBUG] {t('eof_received')}", file=sys.stderr)
                    break
                
                response = handle_request(line)
                if response:
                    print(response)
                    sys.stdout.flush()
                    
            except EOFError:
                print(f"[DEBUG] {t('eof_exception')}", file=sys.stderr)
                break
            except Exception as e:
                print(f"[ERROR] {t('server_error', error=str(e))}", file=sys.stderr)
                print(f"[ERROR] Traceback: {traceback.format_exc()}", file=sys.stderr)
                
    except KeyboardInterrupt:
        print(f"[INFO] {t('server_stopped_by_user')}", file=sys.stderr)
    except Exception as e:
        print(f"[ERROR] {t('fatal_server_error', error=str(e))}", file=sys.stderr)
        print(f"[ERROR] Traceback: {traceback.format_exc()}", file=sys.stderr)

if __name__ == "__main__":
    main()
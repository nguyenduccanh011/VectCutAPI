"""
Local configuration module for loading settings from local config file.

This module loads configuration from config.json file and provides
default values for VectCutAPI server settings.
"""

import os
import json5  # Using json5 instead of standard json module for better flexibility

# Path to the config file
CONFIG_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.json")

# Default settings
# Determines if running in CapCut environment (True) or JianYing (False)
IS_CAPCUT_ENV = True

# Default domain for draft preview
DRAFT_DOMAIN = "https://www.install-ai-guider.top"

# Default preview route endpoint
PREVIEW_ROUTER = "/draft/downloader"

# Whether to upload draft files to cloud storage
IS_UPLOAD_DRAFT = False

# Server port number
PORT = 9000

# Draft folder path (where CapCut/JianYing saves draft files locally)
DRAFT_FOLDER = None

# Object Storage Service (OSS) configuration for video/asset storage
OSS_CONFIG = []
# Separate OSS configuration for MP4 video files
MP4_OSS_CONFIG = []

# Attempt to load local configuration file
if os.path.exists(CONFIG_FILE_PATH):
    try:
        with open(CONFIG_FILE_PATH, "r", encoding="utf-8") as f:
            # Use json5.load for better JSON compatibility (allows comments, trailing commas)
            local_config = json5.load(f)
            
            # Update CapCut/JianYing environment flag
            if "is_capcut_env" in local_config:
                IS_CAPCUT_ENV = local_config["is_capcut_env"]
            
            # Update domain configuration
            if "draft_domain" in local_config:
                DRAFT_DOMAIN = local_config["draft_domain"]

            # Update port number
            if "port" in local_config:
                PORT = local_config["port"]

            # Update preview router endpoint
            if "preview_router" in local_config:
                PREVIEW_ROUTER = local_config["preview_router"]
            
            # Update draft upload flag
            if "is_upload_draft" in local_config:
                IS_UPLOAD_DRAFT = local_config["is_upload_draft"]
                
            # Update OSS (Object Storage Service) configuration
            if "oss_config" in local_config:
                OSS_CONFIG = local_config["oss_config"]
            
            # Update MP4-specific OSS configuration
            if "mp4_oss_config" in local_config:
                MP4_OSS_CONFIG = local_config["mp4_oss_config"]
            
            # Update local draft folder path
            if "draft_folder" in local_config:
                DRAFT_FOLDER = local_config["draft_folder"]

    except Exception as e:
        # If config file fails to load, defaults above will be used
        pass
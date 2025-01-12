import sys
import traceback
import logging
import platform
import subprocess
import os
import json
from typing import Dict, Any, Optional
from datetime import datetime

class TerminalDebugger:
    """Advanced terminal debugging and system information utility"""
    
    @staticmethod
    def get_system_info() -> Dict[str, Any]:
        """Collect comprehensive system information"""
        return {
            "timestamp": datetime.now().isoformat(),
            "os": platform.system(),
            "os_version": platform.version(),
            "os_release": platform.release(),
            "python_version": platform.python_version(),
            "architecture": platform.architecture()[0],
            "processor": platform.processor(),
            "machine": platform.machine(),
            "env_vars": {
                k: v for k, v in os.environ.items() 
                if any(x in k.lower() for x in ['path', 'python', 'home', 'user'])
            }
        }
    
    @staticmethod
    def check_dependencies() -> Dict[str, Optional[str]]:
        """Check critical dependencies and their versions"""
        dependencies = {
            "ffmpeg": ["ffmpeg", "-version"],
            "python": [sys.executable, "--version"],
            "pip": [sys.executable, "-m", "pip", "--version"],
            "torch": [sys.executable, "-c", "import torch; print(torch.__version__)"],
            "whisper": [sys.executable, "-c", "import whisper; print(whisper.__version__)"]
        }
        
        dependency_versions = {}
        for name, cmd in dependencies.items():
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=5, shell=False)
                dependency_versions[name] = result.stdout.strip() or result.stderr.strip()
            except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
                dependency_versions[name] = None
        
        return dependency_versions
    
    @staticmethod
    def capture_exception(e: Exception, additional_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Capture detailed exception information"""
        error_info = {
            "timestamp": datetime.now().isoformat(),
            "type": type(e).__name__,
            "message": str(e),
            "traceback": traceback.format_exc(),
            "system_info": TerminalDebugger.get_system_info(),
            "dependencies": TerminalDebugger.check_dependencies()
        }
        
        if additional_context:
            error_info["context"] = additional_context
        
        return error_info
    
    @staticmethod
    def log_error(error_info: Dict[str, Any], log_file: str = 'debug_log.json'):
        """Log error information to a JSON file"""
        try:
            # Ensure log directory exists
            log_dir = os.path.dirname(log_file) or '.'
            os.makedirs(log_dir, exist_ok=True)
            
            # Read existing logs or create new
            try:
                with open(log_file, 'r') as f:
                    logs = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                logs = []
            
            # Append new error
            logs.append(error_info)
            
            # Write back to file, limit to last 100 entries
            with open(log_file, 'w') as f:
                json.dump(logs[-100:], f, indent=2)
        
        except Exception as log_error:
            logging.error(f"Failed to log error: {log_error}")
    
    @staticmethod
    def export_subtitles_to_srt(subtitles, output_path):
        """Export subtitles to SRT format"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                for i, subtitle in enumerate(subtitles, 1):
                    f.write(f"{i}\n")
                    f.write(f"{subtitle.start_time} --> {subtitle.end_time}\n")
                    f.write(f"{subtitle.text}\n\n")
            return True
        except Exception as e:
            logging.error(f"Failed to export SRT: {e}")
            return False

    @staticmethod
    def diagnose_video_processing_error(video_path: str) -> Dict[str, Any]:
        """Perform detailed diagnosis of video processing error"""
        diagnosis = {
            "video_path": video_path,
            "file_exists": os.path.exists(video_path),
            "file_readable": os.access(video_path, os.R_OK) if os.path.exists(video_path) else False,
            "file_details": None
        }
        
        try:
            if diagnosis["file_exists"]:
                file_stat = os.stat(video_path)
                diagnosis["file_details"] = {
                    "size": file_stat.st_size,
                    "created": file_stat.st_ctime,
                    "modified": file_stat.st_mtime
                }
        except Exception as e:
            diagnosis["file_details_error"] = str(e)
        
        return diagnosis

def global_exception_handler(exc_type, exc_value, exc_traceback):
    """Global exception handler for unhandled exceptions"""
    error_info = TerminalDebugger.capture_exception(exc_value)
    TerminalDebugger.log_error(error_info)
    
    # Print to console
    print("Unhandled Exception Detected:")
    print(f"Type: {exc_type.__name__}")
    print(f"Message: {exc_value}")
    print("Full Traceback:")
    traceback.print_exception(exc_type, exc_value, exc_traceback)

# Set global exception handler
sys.excepthook = global_exception_handler
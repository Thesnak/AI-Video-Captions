import moviepy.editor as mp
from domain.interfaces import VideoProcessor
import pathlib
import tempfile
import logging
import os
import sys
import subprocess
import shutil

# Configure logging
logger = logging.getLogger(__name__)

class FFmpegFinder:
    """Utility class to find FFmpeg executable"""
    _ffmpeg_path = None

    @classmethod
    def find_ffmpeg(cls):
        """Find FFmpeg executable path with comprehensive search"""
        # Skip if already found
        if cls._ffmpeg_path:
            return cls._ffmpeg_path

        # Possible FFmpeg installation paths
        possible_paths = [
            # Standard installation paths
            r"C:\Program Files\FFmpeg\bin\ffmpeg.exe",
            r"C:\Program Files (x86)\FFmpeg\bin\ffmpeg.exe",
            r"C:\ffmpeg\bin\ffmpeg.exe",
            
            # Winget installation paths
            r"C:\Program Files\Gyan\FFmpeg\bin\ffmpeg.exe",
            r"C:\Program Files\VideoLAN\VLC\ffmpeg.exe",
            
            # Path environment variable
            *[os.path.join(path, "ffmpeg.exe") for path in os.environ.get("PATH", "").split(os.pathsep)],
            
            # Additional potential locations
            os.path.expanduser("~\\ffmpeg\\bin\\ffmpeg.exe"),
            r"D:\ffmpeg\bin\ffmpeg.exe",
            r"E:\ffmpeg\bin\ffmpeg.exe"
        ]
        
        # Try using shutil to find FFmpeg in PATH
        ffmpeg_path = shutil.which("ffmpeg")
        if ffmpeg_path:
            possible_paths.append(ffmpeg_path)
        
        # Additional system-wide search
        try:
            # Try using where command to find FFmpeg
            result = subprocess.run(["where", "ffmpeg"], capture_output=True, text=True)
            if result.returncode == 0:
                possible_paths.extend(result.stdout.strip().split('\n'))
        except:
            pass
        
        # Verify FFmpeg executable
        for path in possible_paths:
            try:
                if os.path.exists(path):
                    # Additional verification by running FFmpeg
                    test_cmd = [path, "-version"]
                    result = subprocess.run(test_cmd, capture_output=True, text=True)
                    if result.returncode == 0:
                        logger.debug(f"Found valid FFmpeg at: {path}")
                        cls._ffmpeg_path = path
                        return path
            except Exception as e:
                logger.warning(f"Error checking FFmpeg at {path}: {e}")
        
        logger.error("FFmpeg executable not found. Audio extraction may fail.")
        return None

    @classmethod
    def get_ffmpeg_path(cls):
        """Get cached FFmpeg path or find it"""
        if not cls._ffmpeg_path:
            cls._ffmpeg_path = cls.find_ffmpeg()
        return cls._ffmpeg_path

# Set FFmpeg path if found
FFMPEG_PATH = FFmpegFinder.get_ffmpeg_path()
if FFMPEG_PATH:
    # Set environment variable
    os.environ['FFMPEG_BINARY'] = FFMPEG_PATH
    # Update MoviePy configuration
    try:
        mp.config.change_settings({"FFMPEG_BINARY": FFMPEG_PATH})
    except AttributeError:
        logger.warning("Could not update MoviePy FFmpeg configuration")

class MoviePyVideoProcessor(VideoProcessor):
    def __init__(self):
        # Verify FFmpeg is available during initialization
        self.ffmpeg_path = FFmpegFinder.get_ffmpeg_path()
        if not self.ffmpeg_path:
            logger.warning("FFmpeg not found during initialization")

    async def extract_audio(self, video_path: pathlib.Path) -> pathlib.Path:
        try:
            # Validate input video file
            if not video_path.exists():
                raise FileNotFoundError(f"Video file not found: {video_path}")
            
            # Verify FFmpeg is available
            if not self.ffmpeg_path:
                # Attempt one last time to find FFmpeg
                self.ffmpeg_path = FFmpegFinder.find_ffmpeg()
                
                if not self.ffmpeg_path:
                    raise RuntimeError("FFmpeg is not installed or not found in system PATH")
            
            # Log input video details
            logger.debug(f"Extracting audio from: {video_path}")
            logger.debug(f"Video file size: {os.path.getsize(video_path)} bytes")
            logger.debug(f"Using FFmpeg: {self.ffmpeg_path}")
            
            # Create temporary audio file path
            temp_dir = pathlib.Path(tempfile.gettempdir())
            audio_path = temp_dir / f"{video_path.stem}_audio.wav"
            logger.debug(f"Temporary audio path: {audio_path}")
            
            # Extract audio using FFmpeg directly
            ffmpeg_cmd = [
                self.ffmpeg_path,
                '-i', str(video_path),
                '-vn',  # Disable video
                '-acodec', 'pcm_s16le',  # Audio codec
                '-ar', '16000',  # Sample rate for Whisper
                '-ac', '1',  # Mono channel
                str(audio_path)
            ]
            
            # Run FFmpeg command
            result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
            
            # Check extraction result
            if result.returncode != 0:
                logger.error(f"FFmpeg extraction error: {result.stderr}")
                raise RuntimeError(f"Audio extraction failed: {result.stderr}")
            
            # Verify audio file was created
            if not audio_path.exists():
                raise RuntimeError("Failed to create audio file")
            
            logger.debug(f"Audio extracted successfully. File size: {os.path.getsize(audio_path)} bytes")
            
            return audio_path
        
        except Exception as e:
            logger.error(f"Audio extraction error: {e}", exc_info=True)
            raise

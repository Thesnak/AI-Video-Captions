import whisper
from domain.interfaces import Transcriber, SubtitleEntry
import pathlib
import logging
import os
import subprocess
import sys
import wave
import contextlib

# Configure logging
logger = logging.getLogger(__name__)

def find_ffmpeg():
    """Find FFmpeg executable path"""
    # Common FFmpeg installation paths
    possible_paths = [
        # Standard installation paths
        r"C:\Program Files\FFmpeg\bin\ffmpeg.exe",
        r"C:\Program Files (x86)\FFmpeg\bin\ffmpeg.exe",
        r"C:\ffmpeg\bin\ffmpeg.exe",
        
        # Winget installation path
        r"C:\Program Files\Gyan\FFmpeg\bin\ffmpeg.exe",
        
        # Path environment variable
        *[os.path.join(path, "ffmpeg.exe") for path in os.environ.get("PATH", "").split(os.pathsep)]
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            logger.debug(f"Found FFmpeg at: {path}")
            return path
    
    logger.warning("FFmpeg executable not found. Audio processing may fail.")
    return None

# Global FFmpeg path
FFMPEG_PATH = find_ffmpeg()

class WhisperTranscriber(Transcriber):
    def __init__(self):
        try:
            logger.debug("Loading Whisper model")
            # Verify FFmpeg is available
            if not FFMPEG_PATH:
                logger.warning("FFmpeg not found. Audio processing may be limited.")
            
            # Load Whisper model
            self.model = whisper.load_model("base")
            logger.debug("Whisper model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load Whisper model: {e}", exc_info=True)
            raise

    async def transcribe(self, audio_path: pathlib.Path) -> list[SubtitleEntry]:
        try:
            # Validate input audio file
            if not audio_path.exists():
                raise FileNotFoundError(f"Audio file not found: {audio_path}")
            
            # Log audio file details
            logger.debug(f"Transcribing audio file: {audio_path}")
            logger.debug(f"Audio file size: {os.path.getsize(audio_path)} bytes")
            
            # Validate audio file
            audio_duration = self._get_audio_duration(audio_path)
            if audio_duration <= 0:
                raise ValueError(f"Invalid audio file: {audio_path}")
            
            # Transcribe audio
            logger.debug("Starting transcription")
            result = self.model.transcribe(str(audio_path))
            
            # Validate transcription result
            if not result or 'segments' not in result:
                raise ValueError("No transcription segments found")
            
            # Convert segments to subtitle entries
            subtitles = []
            for i, segment in enumerate(result["segments"]):
                # Skip empty segments
                if not segment["text"].strip():
                    continue
                
                entry = SubtitleEntry(
                    index=i + 1,
                    start_time=self._format_timestamp(segment["start"]),
                    end_time=self._format_timestamp(segment["end"]),
                    text=segment["text"].strip()
                )
                subtitles.append(entry)
            
            # Log transcription results
            logger.debug(f"Transcription completed. Generated {len(subtitles)} subtitle entries")
            
            return subtitles
        
        except Exception as e:
            logger.error(f"Transcription error: {e}", exc_info=True)
            raise

    def _get_audio_duration(self, audio_path: pathlib.Path) -> float:
        """Get audio duration using multiple methods"""
        try:
            # Method 1: Use wave module for WAV files
            if audio_path.suffix.lower() == '.wav':
                with contextlib.closing(wave.open(str(audio_path), 'rb')) as wf:
                    frames = wf.getnframes()
                    rate = wf.getframerate()
                    duration = frames / float(rate)
                    return duration
            
            # Method 2: Use FFmpeg if available
            if FFMPEG_PATH:
                cmd = [
                    FFMPEG_PATH, 
                    '-i', str(audio_path), 
                    '-show_entries', 'format=duration', 
                    '-v', 'quiet', 
                    '-of', 'csv=p=0'
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                try:
                    duration = float(result.stdout.strip())
                    return duration
                except ValueError:
                    logger.warning(f"Could not determine audio duration using FFmpeg: {result.stdout}")
            
            # Method 3: Fallback to file size check
            file_size = os.path.getsize(audio_path)
            if file_size > 0:
                logger.warning("Using file size as a proxy for audio duration")
                return file_size / 1024  # Very rough estimate
            
            return 0
        
        except Exception as e:
            logger.error(f"Audio duration check error: {e}", exc_info=True)
            return 0

    def _format_timestamp(self, seconds: float) -> str:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        msecs = int((seconds * 1000) % 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{msecs:03d}"

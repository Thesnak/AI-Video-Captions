from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional
from enum import Enum
import pathlib

class ProcessingStatus(Enum):
    IDLE = "idle"
    EXTRACTING = "extracting_audio"
    TRANSCRIBING = "transcribing"
    TRANSLATING = "translating"
    COMPLETED = "completed"
    ERROR = "error"

@dataclass
class SubtitleEntry:
    index: int
    start_time: str
    end_time: str
    text: str

class VideoProcessor(ABC):
    @abstractmethod
    async def extract_audio(self, video_path: pathlib.Path) -> pathlib.Path:
        """Extract audio from video file and return path to audio file"""
        pass

class Transcriber(ABC):
    @abstractmethod
    async def transcribe(self, audio_path: pathlib.Path) -> List[SubtitleEntry]:
        """Transcribe audio file to text with timestamps"""
        pass

class Translator(ABC):
    @abstractmethod
    async def translate(self, subtitles: List[SubtitleEntry], target_language: str) -> List[SubtitleEntry]:
        """Translate subtitle entries to target language"""
        pass

class UserPreferences(ABC):
    @abstractmethod
    def save_preferences(self, preferences: dict) -> None:
        pass

    @abstractmethod
    def load_preferences(self) -> dict:
        pass

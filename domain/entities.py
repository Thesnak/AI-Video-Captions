from dataclasses import dataclass
from typing import List, Optional
from domain.interfaces import *

@dataclass
class ProcessingResult:
    status: ProcessingStatus
    message: str
    progress: float
    subtitles: Optional[List[SubtitleEntry]] = None


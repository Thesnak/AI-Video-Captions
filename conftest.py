import pytest
from unittest.mock import Mock
from domain.interfaces import VideoProcessor, Transcriber, Translator

@pytest.fixture
def mock_video_processor():
    processor = Mock(spec=VideoProcessor)
    processor.extract_audio.return_value = Path("test_audio.wav")
    return processor

@pytest.fixture
def mock_transcriber():
    transcriber = Mock(spec=Transcriber)
    transcriber.transcribe.return_value = [
        SubtitleEntry(1, "00:00:01,000", "00:00:02,000", "Test subtitle")
    ]
    return transcriber

@pytest.fixture
def mock_translator():
    translator = Mock(spec=Translator)
    translator.translate.return_value = [
        SubtitleEntry(1, "00:00:01,000", "00:00:02,000", "Test translation")
    ]
    return translator

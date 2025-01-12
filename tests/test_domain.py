import pytest
from pathlib import Path
from domain.interfaces import SubtitleEntry, ProcessingStatus
from domain.entities import ProcessingResult

def test_subtitle_entry_creation():
    entry = SubtitleEntry(
        index=1,
        start_time="00:00:01,000",
        end_time="00:00:02,000",
        text="Hello world"
    )
    assert entry.index == 1
    assert entry.start_time == "00:00:01,000"
    assert entry.end_time == "00:00:02,000"
    assert entry.text == "Hello world"

def test_processing_result_states():
    result = ProcessingResult(
        status=ProcessingStatus.COMPLETED,
        message="Success",
        progress=1.0,
        subtitles=[
            SubtitleEntry(1, "00:00:01,000", "00:00:02,000", "Test")
        ]
    )
    assert result.status == ProcessingStatus.COMPLETED
    assert result.progress == 1.0
    assert len(result.subtitles) == 1

def test_processing_result_error_state():
    error_result = ProcessingResult(
        status=ProcessingStatus.ERROR,
        message="Error occurred",
        progress=0.0
    )
    assert error_result.status == ProcessingStatus.ERROR
    assert error_result.subtitles is None

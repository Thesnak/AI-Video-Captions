import pytest
from application.subtitle_service import SubtitleService

@pytest.mark.asyncio
async def test_subtitle_service_successful_processing(
    mock_video_processor,
    mock_transcriber,
    mock_translator
):
    progress_callback = Mock()
    service = SubtitleService(
        mock_video_processor,
        mock_transcriber,
        mock_translator,
        progress_callback
    )
    
    result = await service.process_video(Path("test.mp4"), "es")
    
    assert result.status == ProcessingStatus.COMPLETED
    assert result.progress == 1.0
    assert len(result.subtitles) == 1
    assert progress_callback.call_count >= 3

@pytest.mark.asyncio
async def test_subtitle_service_error_handling(
    mock_video_processor,
    mock_transcriber,
    mock_translator
):
    mock_video_processor.extract_audio.side_effect = Exception("Test error")
    progress_callback = Mock()
    service = SubtitleService(
        mock_video_processor,
        mock_transcriber,
        mock_translator,
        progress_callback
    )
    
    result = await service.process_video(Path("test.mp4"), "es")
    
    assert result.status == ProcessingStatus.ERROR
    assert result.progress == 0.0
    assert "Test error" in result.message

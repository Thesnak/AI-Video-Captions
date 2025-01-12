from domain.interfaces import VideoProcessor, Transcriber, Translator, ProcessingStatus
from domain.entities import ProcessingResult
from infrastructure.translator import GoogleTranslatorService, ArgosTranslatorService
import pathlib
import asyncio
import logging
from typing import Callable, Optional

# Configure logging
logger = logging.getLogger(__name__)

class SubtitleService:
    def __init__(
        self,
        video_processor: VideoProcessor,
        transcriber: Transcriber,
        translator: Translator,
        progress_callback: Optional[Callable[[ProcessingResult], None]] = None
    ):
        self.video_processor = video_processor
        self.transcriber = transcriber
        self.translators = {
            'GoogleTrans': GoogleTranslatorService(),
            'Argos Translate': ArgosTranslatorService()
        }
        self.progress_callback = progress_callback or (lambda x: None)

    async def process_video(
        self, 
        video_path: pathlib.Path, 
        target_language: str, 
        translation_method: str = 'GoogleTrans'
    ) -> ProcessingResult:
        try:
            logger.debug(f"Starting video processing for {video_path}")
            
            # Validate input
            if not video_path.exists():
                raise FileNotFoundError(f"Video file not found: {video_path}")
            
            # Log translation details
            logger.debug(f"Translating subtitles to {target_language}")
            
            # Validate translation method
            if translation_method not in self.translators:
                logger.warning(f"Unsupported translation method: {translation_method}")
                translation_method = 'GoogleTrans'  # Fallback to default
            
            # Select translator
            translator = self.translators[translation_method]
            
            # Extract audio
            logger.debug("Extracting audio from video")
            self.progress_callback(ProcessingResult(
                status=ProcessingStatus.EXTRACTING,
                message="Extracting audio...",
                progress=0.0
            ))
            audio_path = await self.video_processor.extract_audio(video_path)
            
            logger.debug(f"Audio extracted to {audio_path}")
            
            # Transcribe
            logger.debug("Starting audio transcription")
            self.progress_callback(ProcessingResult(
                status=ProcessingStatus.TRANSCRIBING,
                message="Transcribing audio...",
                progress=0.33
            ))
            subtitles = await self.transcriber.transcribe(audio_path)
            
            logger.debug(f"Transcription completed. Found {len(subtitles)} subtitle entries")
            
            # Translate
            logger.debug(f"Translating subtitles using {translation_method}")
            self.progress_callback(ProcessingResult(
                status=ProcessingStatus.TRANSLATING,
                message="Translating subtitles...",
                progress=0.66
            ))
            
            # Use the specified translation method
            translated_subtitles = await translator.translate(subtitles, target_language)
            
            logger.debug(f"Translation completed. {len(translated_subtitles)} translated subtitles")
            
            return ProcessingResult(
                status=ProcessingStatus.COMPLETED,
                message="Processing completed successfully!",
                progress=1.0,
                subtitles=translated_subtitles
            )
            
        except Exception as e:
            logger.error(f"Video processing error: {e}", exc_info=True)
            return ProcessingResult(
                status=ProcessingStatus.ERROR,
                message=f"Error: {str(e)}",
                progress=0.0
            )

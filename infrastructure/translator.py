from googletrans import Translator as GoogleTranslator
from domain.interfaces import Translator, SubtitleEntry
from typing import List, Optional
import logging
from typing import List, Optional, Callable
from domain.entities import SubtitleEntry
import argostranslate.translate
import asyncio

logger = logging.getLogger(__name__)

class ChunkedTranslator:
    """Advanced translator with chunking and multiple translation methods"""
    
    @staticmethod
    async def chunk_text(text: str, max_chunk_size: int = 500) -> List[str]:
        """Split text into manageable chunks"""
        chunks = []
        current_chunk = []
        current_length = 0
        
        for word in text.split():
            if current_length + len(word) + 1 > max_chunk_size:
                chunks.append(' '.join(current_chunk))
                current_chunk = []
                current_length = 0
            
            current_chunk.append(word)
            current_length += len(word) + 1
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks

class GoogleTranslatorService:
    """Google Translate service with chunked translation"""
    
    def __init__(self, chunk_size: int = 500, timeout: int = 10):
        self.translator = GoogleTranslator()
        self.chunk_size = chunk_size
        self.timeout = timeout
    
    async def translate(
        self, 
        subtitles: List[SubtitleEntry], 
        target_language: str
    ) -> List[SubtitleEntry]:
        """Translate subtitles with chunking and timeout handling"""
        translated_subtitles = []
        
        for subtitle in subtitles:
            try:
                # Chunk the text
                text_chunks = await ChunkedTranslator.chunk_text(subtitle.text, self.chunk_size)
                
                # Translate chunks
                translated_chunks = []
                for chunk in text_chunks:
                    try:
                        # Use asyncio.wait_for to handle timeout
                        translated_chunk = await asyncio.wait_for(
                            self._translate_chunk(chunk, target_language), 
                            timeout=self.timeout
                        )
                        translated_chunks.append(translated_chunk)
                    except asyncio.TimeoutError:
                        logger.warning(f"Translation timeout for chunk: {chunk}")
                        translated_chunks.append(chunk)  # Fallback to original text
                
                # Combine translated chunks
                translated_text = ' '.join(translated_chunks)
                
                # Create new subtitle with translated text
                translated_subtitle = SubtitleEntry(
                    index=subtitle.index,
                    start_time=subtitle.start_time,
                    end_time=subtitle.end_time,
                    text=translated_text
                )
                translated_subtitles.append(translated_subtitle)
            
            except Exception as e:
                logger.error(f"Translation error: {e}")
                # Fallback: keep original subtitle
                translated_subtitles.append(subtitle)
        
        return translated_subtitles
    
    async def _translate_chunk(self, text: str, target_language: str) -> str:
        """Translate a single text chunk"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None, 
            lambda: self.translator.translate(text, dest=target_language).text
        )

class ArgosTranslatorService:
    """Advanced Argos Translate service with comprehensive language support"""
    
    def __init__(self):
        # Language code mapping
        self.language_map = {
            'en': 'en',  # English
            'es': 'es',  # Spanish
            'fr': 'fr',  # French
            'de': 'de',  # German
            'it': 'it',  # Italian
            'pt': 'pt',  # Portuguese
            'ar': 'ar',  # Arabic
        }
        
        # Initialize translation packages
        self._initialize_packages()
    
    def _initialize_packages(self):
        """Download and install necessary translation packages"""
        try:
            # Update package index
            argostranslate.package.update_package_index()
            
            # List of language combinations to download
            language_pairs = [
                ('en', 'es'), ('en', 'fr'), ('en', 'de'),
                ('en', 'it'), ('en', 'pt'), ('en', 'ar')
            ]
            
            for from_code, to_code in language_pairs:
                try:
                    self._download_package(from_code, to_code)
                except Exception as e:
                    logger.warning(f"Failed to download package {from_code}->{to_code}: {e}")
        
        except Exception as e:
            logger.error(f"Package initialization error: {e}")
    
    def _download_package(self, from_code: str, to_code: str):
        """Download translation package if not already installed"""
        available_packages = argostranslate.package.get_available_packages()
        installed_packages = argostranslate.package.get_installed_packages()
        
        # Check if package is already installed
        if any(pkg.from_code == from_code and pkg.to_code == to_code for pkg in installed_packages):
            return
        
        # Find package to download
        package = next(
            (pkg for pkg in available_packages 
             if pkg.from_code == from_code and pkg.to_code == to_code), 
            None
        )
        
        if package:
            package.download()
            package.install()
            logger.info(f"Installed translation package: {from_code}->{to_code}")
    
    async def translate(self, subtitles: List[SubtitleEntry], target_language: str) -> List[SubtitleEntry]:
        """Translate subtitles using Argos Translate"""
        try:
            # Validate target language
            if target_language not in self.language_map:
                logger.warning(f"Unsupported language: {target_language}. Falling back to English.")
                target_language = 'en'
            
            # Convert to Argos language code
            from_code = 'en'
            to_code = self.language_map.get(target_language, 'es')
            
            # Find translation package
            translation_package = self._find_translation_package(from_code, to_code)
            
            if not translation_package:
                logger.error(f"No translation package found for {from_code}->{to_code}")
                return subtitles
            
            # Translate subtitles
            translated_subtitles = []
            for subtitle in subtitles:
                try:
                    # Translate text using the found translation package
                    translated_text = argostranslate.translate.translate(
                        subtitle.text, 
                        from_code, 
                        to_code
                    )
                    
                    translated_subtitle = SubtitleEntry(
                        index=subtitle.index,
                        start_time=subtitle.start_time,
                        end_time=subtitle.end_time,
                        text=translated_text
                    )
                    translated_subtitles.append(translated_subtitle)
                
                except Exception as chunk_error:
                    logger.warning(f"Translation error for subtitle: {chunk_error}")
                    translated_subtitles.append(subtitle)
            
            return translated_subtitles
        
        except Exception as e:
            logger.error(f"Argos translation error: {e}")
            return subtitles
    
    def _find_translation_package(self, from_code: str, to_code: str):
        """Find the most appropriate translation package"""
        installed_packages = argostranslate.package.get_installed_packages()
        
        # First, try direct translation
        direct_package = next(
            (pkg for pkg in installed_packages 
             if pkg.from_code == from_code and pkg.to_code == to_code), 
            None
        )
        
        if direct_package:
            return direct_package
        
        # If direct translation not found, try English as intermediate
        intermediate_packages = [
            pkg for pkg in installed_packages 
            if pkg.from_code == from_code and pkg.to_code == 'en'
        ]
        
        if intermediate_packages:
            logger.info("Using English as intermediate translation language")
            return intermediate_packages[0]
        
        logger.warning(f"No suitable translation package found for {from_code}->{to_code}")
        return None

class MultiTranslator(Translator):
    def __init__(self):
        self.googletrans_translator = GoogleTranslator()
        argostranslate.translate.load_installed_languages()
        self.google_translator_service = GoogleTranslatorService()
        self.argos_translator_service = ArgosTranslatorService()

    def get_translation_methods(self) -> List[str]:
        return ['GoogleTrans', 'Argos']

    async def translate(
        self, 
        subtitles: List[SubtitleEntry], 
        target_language: str, 
        method: str = 'GoogleTrans'
    ) -> List[SubtitleEntry]:
        try:
            if method not in self.get_translation_methods():
                raise ValueError(f"Unsupported translation method: {method}")
            
            translated_subtitles = []
            for subtitle in subtitles:
                translated_text = await self._translate_text(
                    subtitle.text, 
                    target_language, 
                    method
                )
                
                translated_subtitle = SubtitleEntry(
                    index=subtitle.index,
                    start_time=subtitle.start_time,
                    end_time=subtitle.end_time,
                    text=translated_text
                )
                translated_subtitles.append(translated_subtitle)
            
            return translated_subtitles
        
        except Exception as e:
            logger.error(f"Translation error: {e}", exc_info=True)
            raise

    async def _translate_text(
        self, 
        text: str, 
        target_language: str, 
        method: str
    ) -> str:
        try:
            if method == 'GoogleTrans':
                translation = self.googletrans_translator.translate(
                    text, 
                    dest=target_language
                )
                return translation.text
            
            elif method == 'Argos':
                return await self.argos_translator_service.translate([SubtitleEntry(text=text)], target_language)[0].text
            
            else:
                raise ValueError(f"Unsupported translation method: {method}")
        
        except Exception as e:
            logger.error(f"Text translation error: {e}", exc_info=True)
            return text

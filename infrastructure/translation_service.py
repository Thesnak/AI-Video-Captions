# d:/Ai-Video-Captions/infrastructure/translation_service.py
import logging
from typing import List, Optional

# Translation libraries
from googletrans import Translator as GoogleTranslator
import argostranslate.translate

# Configure logging
logger = logging.getLogger(__name__)

class TranslationService:
    def __init__(self):
        # Initialize translation libraries
        self.googletrans_translator = GoogleTranslator()
        
        # Initialize Argos translation
        argostranslate.translate.load_installed_languages()

    def get_available_translation_methods(self) -> List[str]:
        """
        Get available translation methods
        
        Returns:
            List of translation method names
        """
        methods = ['GoogleTrans', 'Argos']
        return methods

    def translate_subtitles(
        self, 
        subtitles: List[dict], 
        target_language: str, 
        method: str = 'GoogleTrans'
    ) -> List[dict]:
        """
        Translate subtitles using specified method
        
        Args:
            subtitles: List of subtitle dictionaries
            target_language: Target language code
            method: Translation method ('GoogleTrans' or 'Argos')
        
        Returns:
            Translated subtitles
        """
        try:
            # Validate method
            if method not in self.get_available_translation_methods():
                raise ValueError(f"Unsupported translation method: {method}")
            
            # Translate each subtitle
            translated_subtitles = []
            for subtitle in subtitles:
                translated_text = self._translate_text(
                    subtitle['text'], 
                    target_language, 
                    method
                )
                
                # Create new subtitle entry with translated text
                translated_subtitle = subtitle.copy()
                translated_subtitle['text'] = translated_text
                translated_subtitles.append(translated_subtitle)
            
            return translated_subtitles
        
        except Exception as e:
            logger.error(f"Translation error: {e}", exc_info=True)
            raise

    def _translate_text(
        self, 
        text: str, 
        target_language: str, 
        method: str
    ) -> str:
        """
        Translate text using specified method
        
        Args:
            text: Text to translate
            target_language: Target language code
            method: Translation method
        
        Returns:
            Translated text
        """
        try:
            if method == 'GoogleTrans':
                # Use GoogleTrans
                translation = self.googletrans_translator.translate(
                    text, 
                    dest=target_language
                )
                return translation.text
            
            elif method == 'Argos':
                # Use Argos translation
                # First, get the installed language
                installed_languages = argostranslate.translate.get_installed_languages()
                
                # Find source and target languages
                source_lang = installed_languages[0]  # Default to first installed language
                target_lang = next(
                    (lang for lang in installed_languages if lang.code == target_language), 
                    None
                )
                
                if not target_lang:
                    raise ValueError(f"Target language {target_language} not installed")
                
                # Perform translation
                translation = argostranslate.translate.translate(
                    text, 
                    source_lang, 
                    target_lang
                )
                return translation
            
            else:
                raise ValueError(f"Unsupported translation method: {method}")
        
        except Exception as e:
            logger.error(f"Text translation error: {e}", exc_info=True)
            return text  # Fallback to original text
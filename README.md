# AI Video Captions
<p align="center">
  <img src="https://github.com/Thesnak/AI-Video-Captions/blob/main/assets/logo.jpg?raw=true" alt="AI-Video-Captions Logo" width="200"/>
</p>

## 🎥 Project Overview
AI Video Captions is an advanced, open-source application for automated video transcription, captioning, and translation using cutting-edge AI technologies.

## ✨ Features
- 🎬 Automated Video Transcription
- 🌐 Multi-language Translation
- 🖥️ User-Friendly Interface
- 🔧 Configurable Preferences
- 💡 AI-Powered Subtitle Generation

## 🛠 Technology Stack
- **Language**: Python 3.9+
- **GUI Framework**: PyQt6
- **Video Processing**: 
  - MoviePy
  - FFmpeg
- **Transcription**: 
  - Whisper (OpenAI)
- **Translation**:
  - GoogleTrans
  - Argos Translate

## Demo Video
![AI Video Captions Demo]([https://user-images.githubusercontent.com/24365953/209460233-6e6b0a7c-8e7f-4da1-87c5-5a7c9c5daa1d.mp4](https://raw.githubusercontent.com/Thesnak/AI-Video-Captions/refs/heads/main/assets/AI%20Video%20Captions%20demo.mp4))


## 🚀 Installation

### Prerequisites
- Python 3.9 or higher
- pip package manager
- FFmpeg

### Clone Repository
```bash
git clone https://github.com/Thesnak/AI-Video-Captions.git
cd AI-Video-Captions
```
### Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Unix/macOS
venv\Scripts\activate     # Windows
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### FFmpeg Installation
#### Windows
1. Chocolatey Installation (Recommended):
```bash
choco install ffmpeg
```

2. Manual Installation:
- Download FFmpeg from [FFmpeg website](https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z) .
- extract the archive to c:\ffmpeg\
- add FFmpeg\bin to PATH environment variable
  
#### Unix/macOS
```bash
brew install ffmpeg # macOS

sudo apt-get install ffmpeg # Ubuntu
```

### 🖥️ Usage
```bash
python main.py
```
### 🔧 Configuration
- Customize translation methods
- Set default language
- Choose application theme

### 🐛 Troubleshooting
- Ensure all dependencies are installed
- Check system requirements
- Review logs in app_debug.log
- Verify FFmpeg installation with ffmpeg -version


### 🤝 Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
 

## 📘 Comprehensive Documentation

### 🏗️ Clean Architecture Overview

#### Architectural Layers
1. **Presentation Layer** (`/presentation`)
   - Responsible for user interface and user interactions
   - Contains UI components, animations, and styling
   - Implements PyQt6 widgets and window management

2. **Application Layer** (`/application`)
   - Manages business logic and use cases
   - Coordinates between domain and infrastructure layers
   - Handles service-level operations like subtitle processing

3. **Domain Layer** (`/domain`)
   - Defines core entities and business rules
   - Contains pure Python classes representing core concepts
   - Independent of frameworks and external libraries

4. **Infrastructure Layer** (`/infrastructure`)
   - Implements external integrations and technical implementations
   - Handles video processing, transcription, and translation
   - Provides concrete implementations of domain interfaces

### 🧩 Key Libraries and Their Roles

#### Video Processing
- **MoviePy**: 
  - Video file manipulation
  - Extracting audio from video
  - Handling multimedia file formats
  - Cross-platform video processing

- **FFmpeg**: 
  - Low-level video and audio processing
  - Codec support
  - Advanced multimedia transformations

#### Transcription
- **Whisper (OpenAI)**:
  - Advanced speech-to-text conversion
  - Multi-language support
  - High accuracy transcription
  - Handles various audio qualities

#### Translation
- **GoogleTrans**:
  - Web-based translation service
  - Multiple language support
  - Quick and lightweight translation

- **Argos Translate**:
  - Offline translation capabilities
  - Open-source translation library
  - Supports multiple language pairs

#### GUI Framework
- **PyQt6**:
  - Modern, responsive UI design
  - Cross-platform compatibility
  - Rich widget library
  - Event-driven programming model

### 🔍 Workflow and Process

#### Video Processing Workflow
1. **Video Selection**
   - User selects video file
   - Validate file format and compatibility

2. **Audio Extraction**
   - Use MoviePy to extract audio
   - Prepare audio for transcription

3. **Transcription**
   - Whisper processes audio
   - Generate initial subtitles/captions

4. **Translation**
   - Apply selected translation method
   - Support multiple target languages
   - Handle chunked translations for large texts

5. **Subtitle Generation**
   - Format and synchronize subtitles
   - Export to various formats (SRT, VTT)

### 🚦 State Management
- Utilizes PyQt6 signals and slots
- Implements asynchronous processing
- Provides real-time progress updates

### 🔒 Error Handling Strategies
- Comprehensive logging
- Graceful error recovery
- User-friendly error messages
- Fallback translation methods

### 🔄 Extensibility
- Modular design allows easy addition of:
  - New translation services
  - Additional transcription models
  - Custom subtitle formats

### 📊 Performance Considerations
- Chunked processing for large files
- Configurable translation batch sizes
- Efficient memory management
- Minimal external API dependencies

### 🌐 Internationalization
- Language code mapping
- Flexible translation method selection
- Support for multiple character sets

### 🔧 Configuration Options
- Theme selection (Light/Dark)
- Default language preferences
- Translation method configuration
- Chunk size customization

### 🧪 Testing Approach
- Unit tests for individual components
- Integration tests for service interactions
- Mock objects for external dependencies
- Continuous integration support

### 🔮 Future Roadmap
- Enhanced AI models
- Real-time translation
- Cloud service integration
- More translation providers
- Improved subtitle styling options
  

### 🖥️ Technical Implementation Details

#### Project Structure
```bash
AI-Video-Captions/
├── main.py                  # Application entry point
├── README.md                # Project documentation
├── requirements.txt         # Python dependencies
├── .gitignore               # Git ignore file

├── domain/                  # Core business logic layer
│   ├── __init__.py
│   ├── entities.py          # Core data models and value objects
│   └── interfaces.py        # Abstract base classes and interfaces

├── application/             # Use case and service layer
│   ├── __init__.py
│   ├── subtitle_service.py  # Subtitle processing business logic
│   └── translation_service.py # Translation management services

├── infrastructure/          # Technical implementation layer
│   ├── __init__.py
│   ├── video_processor.py   # Video and audio processing utilities
│   ├── transcriber.py       # Speech-to-text conversion implementation
│   ├── translator.py        # Translation method implementations
│   └── preferences.py       # Configuration management

├── presentation/            # User interface layer
│   ├── __init__.py
│   ├── main_window.py       # Primary application window
│   ├── styles.py            # UI styling and theming
│   ├── animations.py        # UI interaction animations
│   └── batch_processor.py   # Batch processing UI component

├── tests/                   # Unit and integration tests
│   ├── __init__.py
│   ├── test_video_processor.py
│   ├── test_transcription.py
│   └── test_translation.py

├── assets/                  # Static assets
│   ├── app_icon.png         # Application icon
│   ├── splash_screen.png    # Splash screen image
│   └── logo.jpg             # Logo image

├── logs/                    # Log files
│   ├── app_debug.log
│   └── error.log

└── config/                  # Configuration files
    └── app_config.json
```

### 📦 Layer Responsibilities

#### Domain Layer
- Pure Python classes representing core concepts
- Business logic independent of frameworks
- Defines core entities and interfaces

#### Application Layer
- Implements use cases
- Coordinates between domain and infrastructure
- Contains service-level logic

#### Infrastructure Layer
- Concrete implementations of domain interfaces
- External service integrations
- Technical implementations

#### Presentation Layer
- User interface components
- UI logic and interactions
- Styling and animations

### 🔍 Key Files Explained

#### [main.py](cci:7://file:///d:/Ai-Video-Captions/main.py:0:0-0:0)
- Application entry point
- Initializes core services
- Sets up main application flow

#### `requirements.txt`
- Lists all Python package dependencies
- Enables easy project setup

#### `domain/entities.py`
- Defines core data models
- Subtitle, Video, Translation entities

#### `infrastructure/translator.py`
- Implements translation methods
- Handles different translation providers

#### `presentation/main_window.py`
- Primary application window
- Manages UI components and interactions

### 🛠 Development Conventions
- Each layer is independent
- Dependency injection
- Interface-based design
- Separation of concerns
- SOLID principles

### 📝 Configuration Management
- JSON-based configuration
- Environment-specific settings
- Easy extensibility

### 🧪 Testing Strategy
- Unit tests for individual components
- Integration tests for service interactions
- Mocking external dependencies


#### Dependency Injection Pattern
```python
class SubtitleService:
    def __init__(
        self, 
        video_processor: VideoProcessor,
        transcriber: Transcriber,
        translator: TranslatorService
    ):
        self._video_processor = video_processor
        self._transcriber = transcriber
        self._translator = translator
```

#### Asynchronous Processing
```python
class AsyncVideoProcessor:
    @asyncio.coroutine
    async def process_video(self, video_path: str):
        # Concurrent processing of video components
        audio_extraction = asyncio.create_task(
            self.extract_audio(video_path)
        )
        transcription = asyncio.create_task(
            self.transcribe_audio(await audio_extraction)
        )
        
        # Parallel execution
        audio, subtitles = await asyncio.gather(
            audio_extraction, 
            transcription
        )
```
#### Advanced Error Handling
```python
class TranslationErrorHandler:
    @staticmethod
    def handle_translation_error(
        error: Exception, 
        fallback_methods: List[TranslationMethod]
    ) -> str:
        """
        Implements intelligent error recovery for translations
        
        Args:
            error: Original translation error
            fallback_methods: Alternative translation strategies
        
        Returns:
            Translated text or error message
        """
        for method in fallback_methods:
            try:
                return method.translate()
            except Exception as fallback_error:
                logging.warning(f"Fallback method failed: {fallback_error}")
        
        raise TranslationFailureError("All translation methods exhausted")
```

#### Configuration Management
```python
@dataclass
class AppConfiguration:
    """Centralized configuration management"""
    theme: str = 'dark'
    default_language: str = 'en'
    translation_method: str = 'google'
    chunk_size: int = 500
    
    def save(self, path: str = '~/.app_config.json'):
        """Persist configuration to JSON"""
        with open(path, 'w') as config_file:
            json.dump(asdict(self), config_file)
    
    @classmethod
    def load(cls, path: str = '~/.app_config.json'):
        """Load configuration from JSON"""
        with open(path, 'r') as config_file:
            return cls(**json.load(config_file))

```

#### Performance Monitoring
```python
class PerformanceTracker:
    def __init__(self):
        self.metrics = {
            'video_processing_time': [],
            'transcription_time': [],
            'translation_time': []
        }
    
    def track(self, metric: str, duration: float):
        """Record performance metrics"""
        self.metrics[metric].append(duration)
    
    def get_average(self, metric: str) -> float:
        """Calculate average duration for a metric"""
        return sum(self.metrics[metric]) / len(self.metrics[metric])

```

#### 🔬 Advanced Technical Concepts
- Internationalization Strategy
- Unicode normalization
- Bidirectional text support
- Character set handling
- Locale-aware formatting
#### 🔒 Security Considerations
- Input sanitization
- Secure API key management
- Rate limiting for external services
- Error message obfuscation

#### Scalability Patterns
- Chunked processing
- Lazy loading of resources
- Caching translation results
- Adaptive batch sizing
#### 🔍 Deep Dive: Translation Architecture
Translation Method Interface
```python
class TranslationMethod(ABC):
    @abstractmethod
    async def translate(
        self, 
        text: str, 
        source_lang: str, 
        target_lang: str
    ) -> str:
        """Abstract translation method"""
        pass
```



### 📜 License

MIT License

Copyright (c) 2025 [Thesnak](https://github.com/Thesnak)

Permission is hereby granted, free of charge, to any person obtaining a copy 
of this software and associated documentation files (the "Software"), to deal 
in the Software without restriction, including without limitation the rights 
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
copies of the Software, and to permit persons to whom the Software is 
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR  
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,  
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


### 📞 Contact

- [Thesnak](https://github.com/Thesnak)
- [GitHub](https://github.com/Thesnak/AI-Video-Captions)
- [LinkedIn](https://www.linkedin.com/in/mohamed-thesnak)
- [Email](mailto:mohamed.mahmoud0726@gmail.com)

### 🙏 Acknowledgments

- [MoviePy](https://zulko.github.io/moviepy/)
- [Whisper](https://github.com/openai/whisper) 
- [GoogleTrans](https://pypi.org/project/googletrans/)
- [Argos Translate](https://pypi.org/project/argostranslate/)
- [PyQt6](https://pypi.org/project/PyQt6/)
- [FFmpeg](https://ffmpeg.org/)




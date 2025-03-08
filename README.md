# BrainWavr 🧠🎙️

BrainWavr is a Streamlit application that transforms online articles into professional-sounding podcasts with just a few clicks. Using AI technology, it summarizes article content and recreates it in the natural speaking style of your chosen virtual host.

## Features

- **Instant Podcast Generation**: Convert any online article into a podcast with a single click
- **Multiple Host Options**: Choose from a variety of virtual hosts with different voices and presentation styles
- **Adjustable Content Length**: Select between short, medium, or long podcast formats
- **Downloadable Episodes**: Save your generated podcasts for listening anywhere
- **Episode History**: Access previously generated episodes from the library
- **Customization Options**: Add intro music and outros to your podcasts

## Installation

### Prerequisites
- Python 3.7+
- pip

### Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/brainwavr.git
   cd brainwavr
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create necessary directories:
   ```
   mkdir -p saved_podcasts
   mkdir -p images
   ```

5. Add host images to the `images` directory:
   - jean.png
   - alex.png
   - taylor.png
   - logo.png

## Usage

1. Start the application:
   ```
   streamlit run app.py
   ```

2. Open your web browser and navigate to the address shown in the terminal (typically http://localhost:8501)

3. Using BrainWavr:
   - Select a podcast host
   - Enter the URL of an article you want to convert
   - Click "Generate Podcast"
   - Wait for processing to complete
   - Listen to, download, or share your new podcast

## Project Structure

```
brainwavr/
├── app.py                   # Main Streamlit application
├── api.py                   # API functions for fetching articles and generating content
├── custom_player.py         # Custom audio player implementation
├── requirements.txt         # Python dependencies
├── saved_podcasts/          # Directory for storing generated podcasts
└── images/                  # Host and logo images
    ├── jean.png
    ├── alex.png
    ├── taylor.png
    └── logo.png
```

## API Functions

The application relies on several key functions defined in `api.py`:

- `fetch_article_text(url)`: Extracts the text content from a given article URL
- `generate_summary(text)`: Creates a concise summary of the article appropriate for audio
- `generate_podcast_audio(summary, voice)`: Converts the summary into spoken audio using the selected host's voice

## Customization

You can customize various aspects of the podcasts through the settings sidebar:

- **Podcast Length**: Choose between short (2-3 min), medium (4-6 min), or long (7-10 min) episodes
- **Intro Music**: Toggle inclusion of intro music
- **Outro**: Toggle inclusion of an outro segment

## Contributing

Contributions to BrainWavr are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [Streamlit](https://streamlit.io/) - The web application framework used
- [OpenAI](https://openai.com/) - Text generation capabilities
- [ElevenLabs](https://elevenlabs.io/) - Text-to-speech technology

---

© 2023 BrainWavr
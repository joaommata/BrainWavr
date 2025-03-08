# src/api.py
import anthropic
from langchain_community.llms import HuggingFacePipeline
import torch
import streamlit as st
import numpy as np
import soundfile as sf
from kokoro import KPipeline
import requests
from bs4 import BeautifulSoup
from newspaper import Article
import os
import os
import torch
import numpy as np
import soundfile as sf
import streamlit as st
from kokoro import KPipeline

# Define the podcast directory
PODCAST_DIR = 'podcasts'

# Ensure the podcast directory exists
os.makedirs(PODCAST_DIR, exist_ok=True)

def fetch_article_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    paragraphs = soup.find_all('p')
    article_text = '\n'.join([para.get_text() for para in paragraphs])
    return article_text


def generate_summary(article_text):
    # Create a placeholder for the progress message
    progress_placeholder = st.empty()
    
    prompt = f"""
Hello, Jean! As a professional podcast host recording from your home studio, 
you're about to present an exciting episode summarizing the latest news. Here's the article you'll be discussing:

{article_text}

Deliver this summary in a conversational tone, speaking clearly and confidently. 
Engage your listeners with enthusiasm and authenticity, building rapport as you share your insights. Ensure the episode is informative, high-quality, and reflects your passion for delivering great content. Enjoy the process and look forward to sharing the news with your audience!
Remember, you must reply ONLY with the text for the host to read. Do not include any additional instructions or comments in your response. Thank you!
"""
    # Initialize the Anthropic client
    client = anthropic.Anthropic(api_key="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")

    # Send the prompt to the AI model and receive the response
    answer = client.messages.create(
        model="claude-3-7-sonnet-20250219",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    # Extract and return the summary content
    summary = answer.content
    # Extract the text from the response
    summary = answer.content[0].text         
    print(summary)
    
    # Update the placeholder with a success message
    progress_placeholder.success('✅ Script generated successfully!')
    
    return summary


def generate_podcast_audio(summary_text, article_url, voice='af_heart', sample_rate=24000, save_dir='podcasts'):
    # Create a placeholder for the progress message
    progress_placeholder = st.empty()
    progress_placeholder.info('In the studio, recording podcast...')
    
    # Ensure the save directory exists
    os.makedirs(save_dir, exist_ok=True)
    summary_text = str(summary_text) if not isinstance(summary_text, str) else summary_text

    
    # Generate the episode title using the LLM
    episode_title = fetch_episode_title(article_url)
    
    # Initialize the Kokoro pipeline
    pipeline = KPipeline(lang_code='a')
    audio_segments = []
    
    # Generate audio segments
    generator = pipeline(
        summary_text,
        voice=voice,
        speed=1,
        split_pattern=r'\n+'
    )
    
    for _, _, audio in generator:
        if isinstance(audio, torch.Tensor):
            audio = audio.detach().cpu().numpy()
        audio_segments.append(audio)
    
    if audio_segments:
        full_audio = np.concatenate(audio_segments)
        # Define the filename based on the generated episode title
        filename = f"{save_dir}/{episode_title}.wav"
        # Save the audio file
        sf.write(filename, full_audio, sample_rate)
        
        # Save the script as a text file
        script_filename = f"{save_dir}/{episode_title}.txt"
        with open(script_filename, 'w') as script_file:
            script_file.write(summary_text)
        
        # Update the placeholder with a success message
        progress_placeholder.success('✅ Podcast recorded successfully!')
        
        return filename
    else:
        # Update the placeholder with an error message
        progress_placeholder.error('❌ No audio was generated.')
        raise ValueError("No audio was generated.")


def fetch_episode_title(article_url):
    # Fetch article text and extract title (fallback to URL if no title found)
    title = article_url
    return title.replace(" ", "_")  # Replace spaces with underscores for file safety

    
PODCAST_DIR = 'podcasts'

def display_saved_podcasts():
    # Ensure the podcast directory exists
    os.makedirs(PODCAST_DIR, exist_ok=True)
    
    # List all audio files in the podcast directory
    episodes = [f for f in os.listdir(PODCAST_DIR) if f.endswith('.wav')]
    if episodes:
        st.sidebar.markdown("## Saved Podcasts")
        for episode in episodes:
            episode_name = episode.replace('.wav', '')
            episode_path = os.path.join(PODCAST_DIR, episode)
            script_path = os.path.join(PODCAST_DIR, f"{episode_name}.txt")
            
            with open(episode_path, 'rb') as audio_file:
                audio_bytes = audio_file.read()
            
            # Display the episode name, play button, and delete button
            if st.sidebar.button(f"Play {episode_name}"):
                st.write("Press play to listen")
                st.audio(audio_bytes, format='audio/wav')
    else:
        st.sidebar.markdown("No saved podcasts found.")
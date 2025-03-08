import streamlit as st
from api import fetch_article_text, generate_summary, generate_podcast_audio
from custom_player import display_saved_podcasts, display_custom_audio_player
import os
import time

# Function to display host selection with styled containers
# Function to display host selection with simplified containers
def display_host_selection():
    # Inject custom CSS for styling
    st.markdown("""
        <style>
        .host-container {
            display: flex;
            justify-content: space-around;
            margin-bottom: 20px;
        }
        .host-card {
            width: 100px;
            text-align: center;
            padding: 20px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .host-image {
            width: 60px;
            height: 60px;
            border-radius: 60px;
            object-fit: cover;
            margin: 0 auto 15px auto;
            border: 3px solid white;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        .host-name {
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 5px;
            color: #333;
        }
        .host-description {
            font-size: 14px;
            color: #555;
            margin-bottom: 15px;
            line-height: 1.4;
        }
        .host-card.selected {
            background: #f8f9fa;
            color: #333;
        }
        .select-button {
            border: none;
            padding: 8px 16px;
            border-radius: 20px;
            background-color: #4a90e2;
            color: white;
            font-weight: bold;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        .select-button:hover {
            background-color: #3a7bc8;
        }
        </style>
    """, unsafe_allow_html=True)

    # List of hosts with their details
    hosts = [
        {"name": "Jean", "description": "An engaging host known for insightful interviews and thoughtful analysis.", "image": "jean.png"},
        {"name": "Alex", "description": "Brings fresh perspectives on current events with energy and charisma.", "image": "alex.png"},
        {"name": "Taylor", "description": "Expert in storytelling with a unique flair and warm, inviting tone.", "image": "taylor.png"}
    ]

    # Create a container for host options
    st.markdown("<div class='host-container'>", unsafe_allow_html=True)
    cols = st.columns(3)  # Create three columns
    
    for i, host in enumerate(hosts):
        with cols[i]:
            is_selected = st.session_state.selected_host and st.session_state.selected_host['name'] == host['name']
            
            # Start the card with conditional class
            card_class = "host-card selected" if is_selected else "host-card"
            st.markdown(f"<div class='{card_class}'>", unsafe_allow_html=True)
            
            # Display host image
            st.image(f'images/{host["image"]}', use_container_width=True, output_format="auto")
            
            # Display host information
            st.markdown(f"<div class='host-name'>{host['name']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='host-description'>{host['description']}</div>", unsafe_allow_html=True)
            
            # Add selection button
            button_text = "✓ Selected" if is_selected else f"Select {host['name']}"
            button_style = "background-color: #28a745;" if is_selected else ""
            
            if st.button(button_text, key=f"select_{host['name']}"):
                st.session_state.selected_host = host
                st.rerun()
            
            # Close the card div
            st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)


# Set page config
st.set_page_config(
    page_title="BrainWavr 🎙️",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Display the app title
st.markdown("<h1 class='app-title'>🧠 BrainWavr 🎙️</h1>", unsafe_allow_html=True)
st.markdown("### Turn any article into a professional podcast in seconds")

# Initialize session state variables
if 'selected_host' not in st.session_state:
    st.session_state.selected_host = None
if 'generation_stage' not in st.session_state:
    st.session_state.generation_stage = None
if 'summary_text' not in st.session_state:
    st.session_state.summary_text = None
if 'episode_file' not in st.session_state:
    st.session_state.episode_file = None
if 'currently_playing' not in st.session_state:
    st.session_state.currently_playing = None

# Create a two-column layout
col1, col2 = st.columns([2, 1])

with col1:
    # Display host selection
    st.subheader("🎙️ Choose your podcast host")
    display_host_selection()
    
    # URL input section with enhanced styling
    st.markdown("<div class='url-input-container'>", unsafe_allow_html=True)
    st.subheader("📰 Enter an article URL")
    url = st.text_input("", placeholder="https://example.com/article")
    
    # Only enable the generate button if a host is selected and URL is provided
    generate_disabled = st.session_state.selected_host is None or not url
    generate_button = st.button("🚀 Generate Podcast", disabled=generate_disabled)
    st.markdown("</div>", unsafe_allow_html=True)
        
    if generate_button:
        try:
            # Update the generation stage
            st.session_state.generation_stage = "fetching"
            
            # Fetch article text
            with st.spinner("Fetching article content..."):
                article_text = fetch_article_text(url)
                if not article_text:
                    st.error("Could not fetch the article. Please check the URL and try again.")
                    st.session_state.generation_stage = None
            
            # Update generation stage for summarization
            st.session_state.generation_stage = "summarizing"
            
            # Generate podcast script from the article
            with st.spinner("Creating podcast script..."):
                summary = generate_summary(article_text)
                st.session_state.summary_text = summary
            
            # Update generation stage for podcast generation
            st.session_state.generation_stage = "recording"
            
            # Generate podcast audio
            with st.spinner("Recording podcast with your selected host..."):
                host_voice = st.session_state.selected_host["name"].lower()
                audio_file = generate_podcast_audio(summary, host_voice)
                
                # Extract a simple title from the URL
                article_title = url.split('/')[-1].replace('-', ' ').replace('_', ' ').title()
                if not article_title or article_title.isspace():
                    article_title = "Article"
                
                # Save the file path and episode name in session state
                timestamp = int(time.time())
                filename = f"{host_voice}_podcast_{timestamp}.mp3"
                save_path = os.path.join("saved_podcasts", filename)
                
                st.session_state.episode_name = f"{st.session_state.selected_host['name']}'s Podcast on {article_title}"

                # Ensure directory exists
                os.makedirs("saved_podcasts", exist_ok=True)
                
                # Copy the temporary file to saved_podcasts directory
            with open(audio_file, "rb") as src_file:
                with open(save_path, "wb") as dst_file:
                    dst_file.write(src_file.read())
            
            st.session_state.episode_file = save_path
            
            # Mark as completed
            st.session_state.generation_stage = "completed"
            st.success("Your podcast has been generated successfully!")
            
            # Force a rerun to update the UI with the generated podcast
            st.rerun()
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.session_state.generation_stage = None

with col2:
    # Show the current podcast if available
    if st.session_state.episode_file and st.session_state.summary_text:
        st.subheader("🎧 Your Generated Podcast")
        
        # Display the podcast player
        episode_name = os.path.basename(st.session_state.episode_file).replace('.mp3', '').replace('_', ' ').title()
        display_custom_audio_player(st.session_state.episode_file, st.session_state.episode_name)
        
        # Show the transcript/summary
        with st.expander("📝 View Transcript", expanded=False):
            st.markdown(st.session_state.summary_text)
        
        # Allow downloading the podcast
        with open(st.session_state.episode_file, "rb") as file:
            btn = st.download_button(
                label="⬇️ Download Podcast",
                data=file,
                file_name=os.path.basename(st.session_state.episode_file),
                mime="audio/mpeg"
            )
    
    # Display saved podcasts
    display_saved_podcasts()

# Add a sidebar with app information
with st.sidebar:
    st.title("🧠 About BrainWavr")
    st.write("""
    BrainWavr transforms any article into a professional-sounding podcast with just a few clicks.
    
    **How it works:**
    1. Choose your favorite podcast host
    2. Paste the URL of an article
    3. Click 'Generate Podcast'
    4. Listen, download, and share!
    
    Our AI technology summarizes the content and recreates it in the natural speaking style of the host you selected.
    """)
    
    st.divider()
    
    # Add settings or configuration options
    st.subheader("⚙️ Settings")
    podcast_length = st.select_slider(
        "Podcast Length", 
        options=["Short (2-3 min)", "Medium (4-6 min)", "Long (7-10 min)"],
        value="Medium (4-6 min)"
    )
    
    include_intro = st.checkbox("Include podcast intro music", value=True)
    include_outro = st.checkbox("Include podcast outro", value=True)
    
    st.divider()
    
    # Add a feedback section
    st.subheader("📣 Feedback")
    st.write("We're constantly improving BrainWavr based on your feedback.")
    feedback = st.text_area("Share your thoughts:", placeholder="What did you like? What could be better?")
    if st.button("Submit Feedback"):
        st.success("Thank you for your feedback!")

# Footer
st.markdown("""
<div style="text-align: center; margin-top: 30px; padding: 20px; background-color: #f8f9fa; border-radius: 10px;">
    <p>© 2023 BrainWavr | <a href="#">Privacy Policy</a> | <a href="#">Terms of Service</a></p>
</div>
""", unsafe_allow_html=True)
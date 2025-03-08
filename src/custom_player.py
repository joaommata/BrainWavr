import streamlit as st
import os
from datetime import datetime
import time

def display_custom_audio_player(episode_path, episode_name, script_path=None):
    """
    Display a custom styled audio player for podcast episodes
    """
    with open(episode_path, 'rb') as audio_file:
        audio_bytes = audio_file.read()
    
    # Get file creation time and format it
    creation_time = os.path.getctime(episode_path)
    creation_date = datetime.fromtimestamp(creation_time).strftime('%B %d, %Y')
    
    # Get file size
    file_size = os.path.getsize(episode_path) / (1024 * 1024)  # Convert to MB
    
    # Custom CSS for podcast player
    st.markdown("""
    <style>
    .podcast-player {
        background: linear-gradient(135deg, #2b5876, #4e4376);
        border-radius: 12px;
        padding: 20px;
        margin: 20px 0;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        color: white;
        position: relative;
    }
    .podcast-header {
        display: flex;
        align-items: center;
        margin-bottom: 15px;
    }
    .podcast-icon {
        font-size: 24px;
        margin-right: 15px;
    }
    .podcast-title {
        font-size: 20px;
        font-weight: bold;
    }
    .podcast-metadata {
        display: flex;
        justify-content: space-between;
        margin-bottom: 15px;
        font-size: 14px;
        opacity: 0.8;
    }
    .podcast-controls {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 15px;
    }
    .podcast-button {
        background-color: rgba(255,255,255,0.2);
        border: none;
        color: white;
        padding: 8px 16px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 14px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 20px;
        transition: background-color 0.3s;
    }
    .podcast-button:hover {
        background-color: rgba(255,255,255,0.3);
    }
    .podcast-script {
        background-color: rgba(0,0,0,0.1);
        border-radius: 8px;
        padding: 15px;
        margin-top: 15px;
        max-height: 200px;
        overflow-y: auto;
        font-size: 14px;
        line-height: 1.5;
    }
    .podcast-script-hidden {
        display: none;
    }
    .podcast-waveform {
        height: 60px;
        background: url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxMjAwIDIwMCI+CiAgPHBhdGggZmlsbD0ibm9uZSIgc3Ryb2tlPSJyZ2JhKDI1NSwyNTUsMjU1LDAuMykiIHN0cm9rZS13aWR0aD0iMiIgZD0iTTAsMTAwIEMxMCw4MCAxNSwxMjAgMjAsOTAgQzI1LDYwIDMwLDExMCAzNSw5MCBDNDAsMTEwIDQ1LDgwIDUwLDkwIEM1NSwxMjAgNjAsNjAgNjUsOTAgQzcwLDEyMCA3NSw0MCA4MCw5MCBDODU7MTIwIDkwLDgwIDk1LDkwIEMxMDAsNjAgMTA1LDEyMCAxMTAsOTAgQzExNSw4MCAxMjAsNzAgMTI1LDkwIEMxMzAsODAgMTM1LDkwIDE0MCw5MCBDMTQwLDkwIDE0NSw3MCAxNTAsOTAgQzE1NSwxMTAgMTYwLDgwIDE2NSw5MCBDMTY1LDkwIDE3MCwxMDAgMTc1LDkwIEMxODAsODAgMTg1LDEyMCAxOTAsOTAgQzE5MCw5MCAxOTUsMTAwIDIwMCw5MCI+CiAgICA8YW5pbWF0ZSBhdHRyaWJ1dGVOYW1lPSJkIiBkdXI9IjdzIiByZXBlYXRDb3VudD0iaW5kZWZpbml0ZSIga2V5VGltZXM9IjA7MC4yNTswLjU7MC43NTsxIiB2YWx1ZXM9IgogICAgICBNMCwxMDAgQzEwLDgwIDE1LDEyMCAyMCw5MCBDMjUsNjAgMzAsMTEwIDM1LDkwIEM0MCwxMTAgNDUsODAgNTAsOTAgQzU1LDEyMCA2MCw2MCA2NSw5MCBDNzAsMTIwIDc1LDQwIDgwLDkwIEM4NTsxMjAgOTAsODAgOTUsOTAgQzEwMCw2MCAxMDUsMTIwIDExMCw5MCBDMTEwLDkwIDExNSw4MCAxMjAsOTAgQzEyNSw4MCAxMzAsOTAgMTM1LDkwIEMxNDAsODAgMTQ1LDExMCAxNTAsOTAgQzE1NSw3MCAxNjAsMTAwIDE2NSw5MCBDMTY1LDkwIDE3MCwxMDAgMTc1LDkwIEMxODAsODAgMTg1LDEyMCAxOTAsOTAgQzE5MCw5MCAxOTUsMTAwIDIwMCw5MDsKICAgICAgTTAsMTIwIEMxMCw2MCAxNSwxMzAgMjAsOTAgQzI1LDgwIDMwLDEwMCAzNSw5MCBDNDAsNzAgNDUsMTEwIDUwLDkwIEM1NSw2MCA2MSwxMzAgNjUsOTAgQzcwLDgwIDc1LDEyMCA4MCw5MCBDODU7NjAgOTAsMTMwIDk1LDkwIEMxMDAsODAgMTA1LDExMCAxMTAsOTAgQzExMCw5MCAxMTUsNzAgMTIwLDkwIEMxMjUsMTEwIDEzMCw3MCAxMzUsOTAgQzE0MCwxMTAgMTQ1LDcwIDE1MCw5MCBDMTUwLDkwIDE1NSwxMDAgMTYwLDkwIEMxNjUsODAgMTcwLDEyMCAxNzUsOTAgQzE4MCwxMTAgMTg1LDgwIDE5MCw5MCBDMTkwLDkwIDE5NSwxMDAgMjAwLDkwOwogICAgICBNMCw5MCBDMTAsMTEwIDE1LDcwIDIwLDkwIEMyNSwxMjAgMzAsODAgMzUsOTAgQzQwLDYwIDQ1LDEzMCA1MCw5MCBDNTUsODAgNjAsMTAwIDY1LDkwIEM3MCw4MCA3NSwxMTAgODAsOTAgQzg1OzYwIDkwLDEyMCA5NSw5MCBDMTAwLDEyMCAxMDUsNjAgMTEwLDkwIEMxMTAsOTAgMTE1LDEwMCAxMjAsOTAgQzEyNSw4MCAxMzAsMTEwIDEzNSw5MCBDMTQwLDEyMCAxNDUsNjAgMTUwLDkwIEMxNTAsOTAgMTU1LDcwIDE2MCw5MCBDMTY1LDEyMCAxNzAsNjAgMTc1LDkwIEMxODAsNzAgMTg1LDEyMCAxOTAsOTAgQzE5MCw5MCAxOTUsMTEwIDIwMCw5MDsKICAgICAgTTAsODAgQzEwLDEyMCAxNSw2MCAyMCw5MCBDMjUsMTEwIDMwLDcwIDM1LDkwIEM0MCwxMTAgNDUsNzAgNTAsOTAgQzU1LDExMCA2MCw3MCA2NSw5MCBDNzAsMTEwIDc1LDcwIDgwLDkwIEM4NTs2MCA5MCwxMzAgOTUsOTAgQzEwMCw3MCAxMDUsMTEwIDExMCw5MCBDMTEwLDkwIDExNSwxMDAgMTIwLDkwIEMxMjUsODAgMTMwLDExMCAxMzUsOTAgQzE0MCw4MCAxNDUsMTEwIDE1MCw5MCBDMTUwLDkwIDE1NSw4MCAxNjAsOTAgQzE2NSwxMTAgMTcwLDcwIDE3NSw5MCBDMTgwLDExMCAxODUsNzAgMTkwLDkwIEMxOTAsOTAgMTk1LDEwMCAyMDAsOTA7CiAgICAgIE0wLDEwMCBDMTAsODAgMTUsMTIwIDIwLDkwIEMyNSw2MCAzMCwxMTAgMzUsOTAgQzQwLDExMCA0NSw4MCA1MCw5MCBDNTUsMTIwIDYwLDYwIDY1LDkwIEM3MCwxMjAgNzUsNDAgODAsOTAgQzg1OzEyMCA5MCw4MCA5NSw5MCBDMTAwLDYwIDEwNSwxMjAgMTEwLDkwIEMxMTAsOTAgMTE1LDgwIDEyMCw5MCBDMTIwLDkwIDEyNSw4MCAxMzAsOTAgQzEzNSw4MCAxNDAsOTAgMTQ1LDkwIEMxNTAsODAgMTU1LDExMCAxNjAsOTAgQzE2MCw5MCAxNjUsNzAgMTcwLDkwIEMxNzUsODAgMTgwLDExMCAxODUsOTAgQzE5MCw4MCAxOTUsMTEwIDIwMCw5MDsiCiAgICAgPgogICAgPC9hbmltYXRlPgogIDwvcGF0aD4KPC9zdmc+') repeat-x;
        background-size: 400px 100%;
        margin: 10px 0;
        border-radius: 8px;
        animation: wave-animation 20s linear infinite;
    }
    @keyframes wave-animation {
        0% { background-position-x: 0; }
        100% { background-position-x: 1200px; }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Script content
    script_content = ""
    if script_path and os.path.exists(script_path):
        with open(script_path, 'r') as script_file:
            script_content = script_file.read()
    
    # Format episode name for display (remove underscores, etc.)
    display_name = episode_name.replace('_', ' ').title()
    
    # Generate a container for the podcast player
    st.markdown(f"""
    <div class="podcast-player">
        <div class="podcast-header">
            <div class="podcast-icon">🎙️</div>
            <div class="podcast-title">{display_name}</div>
        </div>
        <div class="podcast-metadata">
            <span>Created: {creation_date}</span>
            <span>Duration: {get_audio_duration(file_size)}</span>
            <span>Size: {file_size:.1f} MB</span>
        </div>
        <div class="podcast-waveform"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Display the actual audio player
    st.audio(audio_bytes, format='audio/wav')
    
    # Display controls for the podcast
    col1, col2, col3 = st.columns([1, 1, 1])
    
    # Show script button
    with col1:
        if st.button("📝 Show Script", key=f"script_{episode_name}"):
            st.session_state[f"show_script_{episode_name}"] = not st.session_state.get(f"show_script_{episode_name}", False)
    
    # Download button
    with col2:
        with open(episode_path, "rb") as file:
            st.download_button(
                label="⬇️ Download",
                data=file,
                file_name=f"{episode_name}.wav",
                mime="audio/wav",
                key=f"download_{episode_name}"
            )
    
    # Delete button
    with col3:
        if st.button("🗑️ Delete", key=f"delete_{episode_name}"):
            st.session_state[f"confirm_delete_{episode_name}"] = True
    
    # Confirmation dialog
    if st.session_state.get(f"confirm_delete_{episode_name}", False):
        st.warning(f"Are you sure you want to delete '{display_name}'?")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Yes, delete it", key=f"confirm_yes_{episode_name}"):
                try:
                    os.remove(episode_path)
                    if script_path and os.path.exists(script_path):
                        os.remove(script_path)
                    st.success(f"Deleted '{display_name}'")
                    time.sleep(1)
                    st.session_state[f"confirm_delete_{episode_name}"] = False
                    st.rerun()
                except Exception as e:
                    st.error(f"Error deleting file: {e}")
        with col2:
            if st.button("No, keep it", key=f"confirm_no_{episode_name}"):
                st.session_state[f"confirm_delete_{episode_name}"] = False
                st.rerun()
    
    # Display script if toggled
    if st.session_state.get(f"show_script_{episode_name}", False) and script_content:
        st.markdown(f"""
        <div class="podcast-script">
            {script_content}
        </div>
        """, unsafe_allow_html=True)


def get_audio_duration(file_size_mb):
    """
    Estimate audio duration based on file size (very approximate)
    For WAV files at 24kHz, 16-bit, mono
    """
    # Approximate duration in minutes (assuming ~2.5MB per minute for WAV 24kHz 16-bit mono)
    approx_minutes = file_size_mb / 2.5
    minutes = int(approx_minutes)
    seconds = int((approx_minutes - minutes) * 60)
    return f"{minutes}:{seconds:02d}"

def display_saved_podcasts(podcast_dir='saved_podcasts'):
    """
    Display saved podcasts with enhanced UI using a simple card-based layout
    with fully integrated buttons
    """
    # Ensure the podcast directory exists
    os.makedirs(podcast_dir, exist_ok=True)
    
    # List all audio files in the podcast directory (both mp3 and wav formats)
    episodes = [f for f in os.listdir(podcast_dir) 
                if f.endswith('.mp3') or f.endswith('.wav')]
    
    if episodes:
        st.sidebar.markdown("## 🎧 **Your Podcast Library**")
        
        # Sort episodes by creation time (newest first)
        episodes.sort(key=lambda x: os.path.getctime(os.path.join(podcast_dir, x)), reverse=True)
        
        # Initialize currently_playing in session state if it doesn't exist
        if 'currently_playing' not in st.session_state:
            st.session_state.currently_playing = None
            
        # Use streamlit's built-in expander as a makeshift "box" solution
        for episode in episodes:
            # Get file extension
            file_ext = os.path.splitext(episode)[1]
            episode_name = episode.replace(file_ext, '')
            episode_path = os.path.join(podcast_dir, episode)
            
            # Format episode name for display - remove timestamp at the end
            if '_' in episode_name:
                # Extract everything before the last underscore (removing timestamp)
                display_name = '_'.join(episode_name.split('_')[:-1])
                display_name = display_name.replace('_', ' ').title()
            else:
                display_name = episode_name.replace('_', ' ').title()
            
            # Get creation date
            creation_time = os.path.getctime(episode_path)
            creation_date = datetime.fromtimestamp(creation_time).strftime('%B %d, %Y')
            
            # Check if this episode is currently selected
            is_selected = st.session_state.currently_playing == episode_name
            
            # Create an expander for each episode (our "box")
            with st.sidebar.expander(f"**{display_name}**", expanded=False):
                # Episode date in the box
                st.markdown(f"<small>Created on {creation_date}</small>", unsafe_allow_html=True)
                
                # Play button inside the expander (our "box")
                if st.button("🎧 Listen", key=f"play_{episode_name}", use_container_width=True):
                    st.session_state.currently_playing = episode_name
                    st.rerun()
                    
            # Style the expander to look like our box
            if is_selected:
                st.markdown("""
                <style>
                    /* Style for selected episode */
                    .streamlit-expanderHeader:hover {
                        background-color: #e0f7fa !important;
                    }
                    .streamlit-expanderHeader {
                        background-color: #e0f7fa !important;
                        border-left: 5px solid #26c6da !important;
                        border-radius: 10px !important;
                    }
                </style>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <style>
                    /* Style for non-selected episodes */
                    .streamlit-expanderHeader:hover {
                        background-color: #f0f0f0 !important;
                    }
                    .streamlit-expanderHeader {
                        background-color: #f5f5f5 !important;
                        border-radius: 10px !important;
                    }
                </style>
                """, unsafe_allow_html=True)
    else:
        st.sidebar.markdown("## 🎧 Your Podcast Library")
        st.sidebar.markdown("No saved podcasts found. Generate your first podcast!")
        
    # Display the currently playing episode in the main area if selected
    if hasattr(st.session_state, 'currently_playing') and st.session_state.currently_playing:
        episode_name = st.session_state.currently_playing
        # Check file extension
        if os.path.exists(os.path.join(podcast_dir, f"{episode_name}.mp3")):
            episode_path = os.path.join(podcast_dir, f"{episode_name}.mp3")
            script_path = os.path.join(podcast_dir, f"{episode_name}.txt")
        else:
            episode_path = os.path.join(podcast_dir, f"{episode_name}.wav")
            script_path = os.path.join(podcast_dir, f"{episode_name}.txt")
        
        if os.path.exists(episode_path):
            st.markdown("## 🎧 Now Playing")
            # Format display name from filename
            if '_' in episode_name:
                # Extract everything before the last underscore (removing timestamp)
                display_name = '_'.join(episode_name.split('_')[:-1])
                display_name = display_name.replace('_', ' ').title()
            else:
                display_name = episode_name.replace('_', ' ').title()
                
            display_custom_audio_player(episode_path, display_name, script_path if os.path.exists(script_path) else None)
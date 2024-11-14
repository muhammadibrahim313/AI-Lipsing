import streamlit as st
import os
import requests
import torch
from google.colab import drive

# GitHub repository URL
GITHUB_REPO_URL = "https://github.com/aHmiicH17/lipsync-lab"
UPLOAD_FOLDER = 'result_output'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Function to download files from GitHub
def download_from_github(file_path):
    url = f"{GITHUB_REPO_URL}/raw/main/{file_path}"
    local_path = f"lipsync-lab/{file_path}"
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    response = requests.get(url)
    with open(local_path, "wb") as file:
        file.write(response.content)
    return local_path

# Download necessary files from GitHub
if not os.path.exists('lipsync-lab'):
    os.makedirs('lipsync-lab')
    download_from_github("checkpoints/mobilenet.pth")
    download_from_github("models/wav2lip.py")
    # Add any additional files needed for the model here

# Mount Google Drive (if in Colab)
if not os.path.exists('/content/drive'):
    drive.mount('/content/drive')

# Define setup and upload functions
def setup_environment():
    # Install additional dependencies if needed
    os.system('pip install batch_face basicsr==1.4.2 gfpgan')
    os.system('python lipsync-lab/install.py')
    st.success("Setup complete. You can now upload your files.")

def upload_audio(audio_file):
    if audio_file is not None:
        audio_path = os.path.join(UPLOAD_FOLDER, audio_file.name)
        with open(audio_path, "wb") as f:
            f.write(audio_file.getbuffer())
        st.success(f"Audio file '{audio_file.name}' uploaded successfully!")
    else:
        st.error("No audio file uploaded.")

def upload_video(video_file):
    if video_file is not None:
        video_path = os.path.join(UPLOAD_FOLDER, video_file.name)
        with open(video_path, "wb") as f:
            f.write(video_file.getbuffer())
        st.success(f"Video file '{video_file.name}' uploaded successfully!")
    else:
        st.error("No video file uploaded.")

# Streamlit Interface Layout
st.title("AI Lip-Sync Application")

# Setup tab
st.header("Setup Environment")
if st.button("Run Setup"):
    setup_environment()

# Upload files tab
st.header("Upload Files")
audio_file = st.file_uploader("Upload Audio File", type=["wav", "mp3"])
if st.button("Upload Audio"):
    upload_audio(audio_file)

video_file = st.file_uploader("Upload Video File", type=["mp4"])
if st.button("Upload Video"):
    upload_video(video_file)

# Settings tab (for future configurations if needed)
st.header("Settings")
st.write("Additional settings can be added here.")

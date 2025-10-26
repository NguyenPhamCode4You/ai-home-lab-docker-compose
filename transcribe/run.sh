#!/bin/bash
set -e  # Exit on error

# Update package list
apt-get update

# Install system dependencies for audio/video processing
apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libsndfile1 \
    ffmpeg \
    python3-pip

# Install Python dependencies
pip3 install -r requirements.txt

echo "Setup complete! You can now run: python3 run.py <video_file.mp4>"
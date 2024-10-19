#!/bin/bash

# Download and configure CUDA repository pinning
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2404/x86_64/cuda-ubuntu2404.pin
sudo mv cuda-ubuntu2404.pin /etc/apt/preferences.d/cuda-repository-pin-600

# Download the CUDA local installer
wget https://developer.download.nvidia.com/compute/cuda/12.6.2/local_installers/cuda-repo-ubuntu2404-12-6-local_12.6.2-560.35.03-1_amd64.deb

# Install the CUDA repository
sudo dpkg -i cuda-repo-ubuntu2404-12-6-local_12.6.2-560.35.03-1_amd64.deb

# Copy the GPG keyring for the CUDA repository
sudo cp /var/cuda-repo-ubuntu2404-12-6-local/cuda-*-keyring.gpg /usr/share/keyrings/

# Update the package list
sudo apt-get update

# Install the CUDA toolkit
sudo apt-get -y install cuda-toolkit-12-6

echo "CUDA Toolkit 12.6 installed successfully."

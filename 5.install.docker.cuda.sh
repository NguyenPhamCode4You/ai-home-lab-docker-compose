#!/bin/bash

# Clone the GitHub repository
git clone --recurse-submodules https://github.com/NguyenPhamCode4You/ai-home-lab-docker-compose.git

# Display NVIDIA GPU status
nvidia-smi

# Add NVIDIA container toolkit GPG key and repository
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

# Update package list and install NVIDIA container toolkit
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit

# Configure the NVIDIA container runtime for Docker
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker

echo "Setup complete!"

#!/bin/bash

# Set the HOME environment variable (adjust path if necessary)
export HOME="/root"  # or /path/to/home
export DOTNET_CLI_HOME="$HOME"

# Set up the working directory
WORKDIR="/config"
mkdir -p "$WORKDIR"
cd "$WORKDIR" || exit

# Update and install dependencies for nvm, Node.js, yarn, and .NET SDK
apt-get update && \
apt-get install -y curl wget build-essential libssl-dev zlib1g-dev \
    ca-certificates gnupg && \
apt-get clean && \
rm -rf /var/lib/apt/lists/*

# Install Node.js 20 and npm, and then yarn
curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
apt-get install -y nodejs && \
npm install -g npm && \
npm install -g yarn

# Verify installation of Node.js, npm, and yarn
node -v
npm -v
yarn -v

# Install .NET SDK 8.0
apt-get update && \
apt-get install -y dotnet-sdk-8.0

# Expose the necessary ports (this is just a note since ports can't be exposed in a script)
echo "Remember to expose port 8443 when running the container."

# Change to the workspace directory
WORKSPACE_DIR="$WORKDIR/workspace"
mkdir -p "$WORKSPACE_DIR"
cd "$WORKSPACE_DIR" || exit

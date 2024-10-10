FROM lscr.io/linuxserver/code-server:latest

# Set up your working directory and environment variables
WORKDIR /config

# Install dependencies for nvm, Node.js, yarn, and .NET SDK
RUN apt-get update && \
    apt-get install -y curl wget build-essential libssl-dev zlib1g-dev \
    ca-certificates gnupg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install nvm, Node.js 20, and npm in a single RUN command
# Install Node.js 20, npm, and yarn without nvm
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g npm && \
    npm install -g yarn

# Verify installation of Node.js, npm, and yarn
RUN node -v && npm -v && yarn -v

# Install .NET SDK 8.0
RUN apt-get update && \
    apt-get install -y dotnet-sdk-8.0

# Expose the necessary ports (you can customize these)
EXPOSE 8443

WORKDIR /config/workspace
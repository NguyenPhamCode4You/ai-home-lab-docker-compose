#!/bin/bash

# Create the code-server directory
mkdir -p ~/code-server && cd ~/code-server

# Download code-server
wget https://github.com/coder/code-server/releases/download/v4.8.2/code-server-4.8.2-linux-amd64.tar.gz

# Extract the downloaded tarball
tar -xzvf code-server-4.8.2-linux-amd64.tar.gz

# Copy the extracted files to /usr/lib/code-server
sudo cp -r code-server-4.8.2-linux-amd64 /usr/lib/code-server

# Create a symbolic link to the code-server binary
sudo ln -s /usr/lib/code-server/bin/code-server /usr/bin/code-server

# Create the directory for code-server data
sudo mkdir -p /var/lib/code-server

# Create the systemd service file
cat <<EOL | sudo tee /lib/systemd/system/code-server.service
[Unit]
Description=code-server
After=nginx.service

[Service]
Type=simple
Environment=PASSWORD=123456
ExecStart=/usr/bin/code-server --bind-addr 10.13.13.4:8441 --user-data-dir /var/lib/code-server
Restart=always

[Install]
WantedBy=multi-user.target
EOL

# Start and enable the code-server service
sudo systemctl start code-server
sudo systemctl enable code-server
sudo systemctl status code-server



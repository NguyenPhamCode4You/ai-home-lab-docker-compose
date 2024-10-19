# Update the package list
sudo apt update

# Install WireGuard
sudo apt install -y wireguard

# Create a systemd service for WireGuard to run at startup
echo "[Unit]
Description=WireGuard Peer3
After=network.target

[Service]
ExecStart=/usr/bin/wg-quick up /home/$(whoami)/Download/peer3.conf
ExecStop=/usr/bin/wg-quick down /home/$(whoami)/Download/peer3.conf
Type=simple
Restart=on-failure

[Install]
WantedBy=multi-user.target" | sudo tee /etc/systemd/system/wg-peer3.service

# Enable the service to run at startup
sudo systemctl enable wg-peer3.service
sudo systemctl start wg-peer3.service

echo "WireGuard installation complete and configured to start on boot."
#!/bin/bash

# Update package lists
sudo apt update

# Install required dependencies
sudo apt install -y wget gnupg

# Add Google Chrome's signing key and repository
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google-chrome.list

# Update package lists again and install Google Chrome
sudo apt update
sudo apt install -y google-chrome-stable

# Install Python dependencies
pip install --user -r requirements.txt

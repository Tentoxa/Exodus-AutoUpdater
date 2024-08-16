# 🐍 Exodus Updater Script

<p align="center">
  A Python script to automatically check for the latest version of Exodus, download, and install it on your Linux system.
</p>

## Features

- **Automatic Version Check**: Compares the installed version of Exodus with the latest available version.
- **Seamless Download**: Downloads the latest version if an update is available.
- **Easy Installation**: Uses `dpkg` for installation, requiring minimal user intervention.

## Prerequisites

- Python 3.x
- `curl_cffi` library for making HTTP requests
- `BeautifulSoup` for parsing HTML
- `tqdm` for displaying progress bars
- `dpkg` for package management on Debian-based systems

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/exodus-updater.git
   cd exodus-updater
   ```
2. **Install required Python packages**:

   ```bash
   pip install -r requirements.txt
   ```
3. **Usage**:

   ```bash
   python exodus_updater.py
   ```

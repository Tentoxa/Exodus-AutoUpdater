from curl_cffi import requests
import os
from tqdm import tqdm
from bs4 import BeautifulSoup
import time
import subprocess

session = requests.Session(impersonate="chrome")

link = "https://downloads.exodus.com/releases/exodus-linux-x64-%version%.deb"
temp_dir = "temp"

def log(message):
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {message}")

def get_latest_version():
    response = session.get('https://www.exodus.com/releases/')
    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')

    version_element = soup.find('span', class_='x-releases__item-heading-date')

    if version_element:
        version_number = version_element.get_text(strip=True)
        log(f"Latest version: {version_number}")
        return version_number
    
def get_installed_version():
    # Run dpkg command and capture output
    output = os.popen("dpkg -l | grep exodus").read()
    
    if "exodus" in output:
        # Split the output by whitespace and extract the version number (3rd column)
        version_number = output.split()[2]
        if(version_number):
            version_number = version_number.split("-")[0]
            log(f"Installed version: {version_number}")
        return version_number
    else:
        print("Exodus not installed.")
        return None


def download_file(download_link, temp_dir):
    """
    Downloads a file from the given link and saves it to the specified directory.

    Parameters:
    - download_link (str): The URL of the file to download.
    - temp_dir (str): The directory where the file will be saved.

    Returns:
    - str: The path to the downloaded file.
    """
    response = session.get(download_link, stream=True)
    filename = download_link.split("/")[-1]
    file_path = os.path.join(temp_dir, filename)

    # Get the total file size from the response headers
    total_size = int(response.headers.get('content-length', 0))

    log("Downloading...")

    # Use tqdm to display the progress bar
    with open(file_path, 'wb') as f, tqdm(
        desc=filename,
        total=total_size,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for chunk in response.iter_content():
            f.write(chunk)
            bar.update(len(chunk))

    log(f"Download completed: {file_path}")
    return file_path
    
latest_version = get_latest_version()
if(not latest_version):
    log("Failed to retrieve latest version number.")
    quit()
installed_version = get_installed_version()

if(not installed_version):
    log("Exodus not installed. Skipping update check.")
else:
    if(latest_version == installed_version):
        log("Exodus is up to date.")
        quit()


download_link = link.replace("%version%", latest_version)
log("Download link: "+download_link)

current_dir = os.path.dirname(os.path.realpath(__file__))
temp_dir = os.path.join(current_dir, temp_dir)
os.makedirs(temp_dir, exist_ok=True)
file_path = download_file(download_link, temp_dir)

log("Downloaded to: "+file_path)
log("Installing...")

log("\033[93mPlease enter your password to install the package\033[0m")

subprocess.run(f"sudo dpkg -i {file_path}", shell=True, check=True)
os.remove(file_path)

log("Installation completed.")

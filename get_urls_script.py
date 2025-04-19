import requests
import os

# Configuration
REPO_OWNER = "toekneema"
REPO_NAME = "Vogue-Runway-Photo-Favorites"
BRANCH = "master"
OUTPUT_FILE = "urls.txt"

# GitHub API URL to list contents of a folder
def get_folder_contents(folder_path=""):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{folder_path}?ref={BRANCH}"
    # Add PAT if needed: headers = {"Authorization": "token your_personal_access_token"}
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

# Generate raw URL for a file
def get_raw_url(file_path):
    return f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/{BRANCH}/{file_path}"

# Recursively scan for image files
def scan_for_pngs(folder_path=""):
    raw_urls = []
    try:
        contents = get_folder_contents(folder_path)
        for item in contents:
            if item["type"] == "file" and item["name"].lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
                file_path = item["path"].replace(" ", "%20")
                raw_url = get_raw_url(file_path)
                raw_urls.append(raw_url)
            elif item["type"] == "dir":
                subfolder_path = item["path"]
                raw_urls.extend(scan_for_pngs(subfolder_path))
    except Exception as e:
        print(f"Error processing folder {folder_path}: {e}")
    return raw_urls

# Main function to generate urls.txt
def generate_list():
    raw_urls = scan_for_pngs()
    with open(OUTPUT_FILE, "w") as f:
        for url in raw_urls:
            f.write(url + "\n")
    print(f"Overwrote {OUTPUT_FILE} with {len(raw_urls)} URLs.")

# Run the script
if __name__ == "__main__":
    generate_list()
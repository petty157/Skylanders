import os
import requests

# ANSI escape code for colors
RED = '\033[91m'    # Red
GREEN = '\033[92m'  # Green
CYAN = '\033[96m'   # Cyan
YELLOW = '\033[93m' # Yellow
RESET = '\033[0m'   # Reset
ORANGE = '\033[33m' # Orange

# Print the note
print(ORANGE + "Script created by Winnernombre and edited by Petty157" + RESET)
print(ORANGE + "Note: This script is for the Android version of the game." + RESET)

# Prompt the user for the download directory path
while True:
    path = input("Enter the download directory path: ").rstrip('\\') + '\\'
    if os.path.exists(path):
        break
    else:
        print(RED + "Download path is incorrect. Please enter a valid directory path." + RESET)
        time.sleep(4)

# List of available languages
available_languages = {
    "English": {"identifier": "", "total_files": None},  # Set total_files to None for English
    "Dutch": {"identifier": "dutch", "total_files": 634},
    "Finnish": {"identifier": "finnish", "total_files": 634},
    "French": {"identifier": "french", "total_files": 634},
    "German": {"identifier": "german", "total_files": 634},
    "Hispanic": {"identifier": "hispanic", "total_files": 634},
    "Italian": {"identifier": "italian", "total_files": 634},
    "Norwegian": {"identifier": "norwegian", "total_files": 634},
    "Portuguese": {"identifier": "portuguese", "total_files": 634},
    "Spanish": {"identifier": "spanish", "total_files": 634},
    "Swedish": {"identifier": "swedish", "total_files": 634},
    "Danish": {"identifier": "danish", "total_files": 634},
}

# Prompt the user to select a language for filtering the downloads
print("Available languages:")
for i, lang in enumerate(available_languages.keys(), 1):
    print(f"{i}. {lang}")

while True:
    selected_language = input("Select a language to download (enter the corresponding number): ")
    if selected_language.isdigit():
        selected_language = int(selected_language)
        if selected_language not in range(1, len(available_languages) + 1):
            print(RED + "Invalid number! Please enter a number between 1 and 12." + RESET)
        else:
            break
    else:
        print(RED + "Invalid input! Please enter a number." + RESET)

selected_language = list(available_languages.keys())[selected_language - 1]
language_identifier = available_languages[selected_language]["identifier"]
total_files = available_languages[selected_language]["total_files"]

URL = "http://trapteam-tablet.activision.com/Tablet2014/andb/ContentDeploymentManifest.xml.D4C088857665CFB8E70CD26EFAC483D7"
response = requests.get(URL)

text = response.text.split("\n")
text = [i for i in text if "http://trapteam-tablet.activision.com/" in i]

# Count total files for the specified language
remaining_files = total_files

for index, i in enumerate(text, start=1):
    link = i[i.find("http://trapteam-tablet.activision.com/"):-8]
    filename_with_hash = link.split('/')[-1]  # Extracts the filename with hash from the URL

    # Filter files by language and extract filename
    if language_identifier == "" or language_identifier in filename_with_hash:
        filename = filename_with_hash

        # Check if file already exists
        if os.path.exists(os.path.join(path, filename)):
            print(f"{YELLOW}[SKIPPED    ]{RESET} {filename} (File already exists)")
            continue

        print(link)
        # Display "BEGIN" in red
        print(RED + "[BEGIN     ]" + RESET, filename)

        # Download the file
        getlink = requests.get(link, stream=True)
        file_size = int(getlink.headers.get('content-length')) if getlink.headers.get('content-length') else 0
        downloaded = 0

        with open(os.path.join(path, filename), "wb") as file:
            for data in getlink.iter_content(chunk_size=1024):
                file.write(data)
                downloaded += len(data)
                percent = round((downloaded / file_size) * 100, 2) if file_size > 0 else 100
                # Display percentage in cyan
                print(f"\r{CYAN}Progress: {percent}%{RESET}", end="", flush=True)

        # Display "DOWNLOADED" in green
        print(GREEN + "\r[DOWNLOADED]" + RESET, filename)

print(f"\n\nFINISHED DOWNLOADING {selected_language} language.")
print(GREEN + "Download finished!" + RESET)
print(ORANGE + "To exit, please press 0." + RESET)
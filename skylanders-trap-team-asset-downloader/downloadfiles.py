import os
import time
import requests

RED = '\033[91m'
GREEN = '\033[92m'
CYAN = '\033[96m'
YELLOW = '\033[93m'
RESET = '\033[0m'
ORANGE = '\033[33m'

print(ORANGE + "Script created by Winnernombre and edited by Petty157" + RESET)
print(ORANGE + "Note: This script is for the Android version of the game." + RESET)

while True:
    path = input("Enter the download directory path: ").rstrip('\\') + '\\'
    if os.path.exists(path):
        break
    else:
        print(RED + "Download path is incorrect. Please enter a valid directory path." + RESET)
        time.sleep(4)

available_languages = {
    "English": "",
    "Dutch": "dutch",
    "Finnish": "finnish",
    "French": "french",
    "German": "german",
    "Hispanic": "hispanic",
    "Italian": "italian",
    "Norwegian": "norwegian",
    "Portuguese": "portuguese",
    "Spanish": "spanish",
    "Swedish": "swedish",
    "Danish": "danish",
}

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
language_identifier = available_languages[selected_language]

URL = "http://trapteam-tablet.activision.com/Tablet2014/andb/ContentDeploymentManifest.xml.D4C088857665CFB8E70CD26EFAC483D7"
response = requests.get(URL)

text = response.text.split("\n")
text = [i for i in text if "http://trapteam-tablet.activision.com/" in i]

for i in text:
    link = i[i.find("http://trapteam-tablet.activision.com/"):-8]
    filename_with_hash = link.split('/')[-1]

    if language_identifier == "" or language_identifier in filename_with_hash:
        filename = filename_with_hash

        if os.path.exists(os.path.join(path, filename)):
            print(f"{YELLOW}[SKIPPED    ]{RESET} {filename} (File already exists)")
            continue

        print(link)
        print(RED + "[BEGIN     ]" + RESET, filename)

        getlink = requests.get(link, stream=True)
        file_size = int(getlink.headers.get('content-length')) if getlink.headers.get('content-length') else 0
        downloaded = 0

        with open(os.path.join(path, filename), "wb") as file:
            for data in getlink.iter_content(chunk_size=1024):
                file.write(data)
                downloaded += len(data)
                percent = round((downloaded / file_size) * 100, 2) if file_size > 0 else 100
                print(f"\r{CYAN}Progress: {percent}%{RESET}", end="", flush=True)

        print(GREEN + "\r[DOWNLOADED]" + RESET, filename)

print(f"\n\nFINISHED DOWNLOADING {selected_language} language.")
print(GREEN + "Download finished!" + RESET)
print(ORANGE + "To exit, please press 0." + RESET)

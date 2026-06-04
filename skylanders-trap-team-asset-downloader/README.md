# Skylanders Trap Team — Server Files Downloader

Downloads official **Skylanders Trap Team** tablet content from Activision’s legacy CDN for the **Android** build. The script reads the content deployment manifest, filters assets by language, and saves them to a folder you choose.

> **Android only.** This manifest and URL path target the `andb` (Android) tablet deployment, not iOS.

## Credits

- **Winnernombre** — original script
- **Petty157** — edits and maintenance

## Requirements

- Python 3.6+
- [`requests`](https://pypi.org/project/requests/)

```bash
pip install requests
```

## Usage

1. Open a terminal in this folder.
2. Run the script:

   ```bash
   python downloadfiles.py
   ```

3. Enter a **valid existing directory** where files should be saved (e.g. `C:\TrapTeam\assets\`).
4. Pick a **language** from the numbered list (1–12).
5. Wait while files download. Existing files in the target folder are **skipped**.

The script prints colored status lines: begin, progress %, downloaded, or skipped.

## Supported languages

| # | Language   | Manifest filter |
|---|------------|-----------------|
| 1 | English    | (default / all matching entries) |
| 2 | Dutch      | `dutch` |
| 3 | Finnish    | `finnish` |
| 4 | French     | `french` |
| 5 | German     | `german` |
| 6 | Hispanic   | `hispanic` |
| 7 | Italian    | `italian` |
| 8 | Norwegian  | `norwegian` |
| 9 | Portuguese | `portuguese` |
| 10 | Spanish   | `spanish` |
| 11 | Swedish   | `swedish` |
| 12 | Danish    | `danish` |

Non-English packs are filtered by a language tag in each asset filename on the CDN.

## How it works

1. Fetches Activision’s **ContentDeploymentManifest** for Trap Team tablet Android builds.
2. Parses manifest lines that contain `http://trapteam-tablet.activision.com/`.
3. For each asset URL, derives the on-disk filename (hash suffix included).
4. Downloads missing files with streaming and a simple progress percentage.

Manifest source (example):

`http://trapteam-tablet.activision.com/Tablet2014/andb/ContentDeploymentManifest.xml.D4C088857665CFB8E70CD26EFAC483D7`

## Notes

- **Resume-friendly:** re-running the script skips files already present in your folder.
- **Network:** requires access to `trapteam-tablet.activision.com`. If Activision has shut down or changed these endpoints, downloads may fail.
- **Legal:** assets are Activision’s property. Use only for preservation, modding, or research you are allowed to perform; this repo does not grant any license to the game files.

## Project layout

```
.
├── downloadfiles.py   # Interactive downloader
└── README.md
```

## License

No license is specified for this script. Game assets remain subject to Activision’s terms.

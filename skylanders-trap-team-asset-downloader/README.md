# Skylanders Trap Team — Android Language Files Downloader

Downloads **Skylanders Trap Team** Android tablet assets from Activision’s legacy CDN manifest, with filters tuned for **language packs** and **English base content** (not a full blind manifest dump).

> **Android only.** Uses the `andb` tablet deployment manifest, not iOS.

## Credits

- **Winnernombre** — original script
- **Petty157** — edits and maintenance

## Requirements

- Python 3.6+
- [`requests`](https://pypi.org/project/requests/)

```bash
pip install -r requirements.txt
```

## Usage

1. Open a terminal in this folder.
2. Run:

   ```bash
   python downloadfiles.py
   ```

3. Enter an **existing** folder path where files should be saved.
4. Choose a language (1–12).
5. Wait for downloads. Files already on disk are skipped (English shows progress against the expected total).

## Language filtering

| # | Language | What gets downloaded |
|---|----------|----------------------|
| 1 | **English** | Filenames containing `level` or `character` (~526 assets). Shows a running **downloaded/total** counter for English. |
| 2–12 | **Other languages** | Filename contains the language tag (`dutch`, `french`, etc.) and does **not** contain `english`. |

This avoids pulling unrelated manifest entries for English and avoids mixing English-tagged files into other language packs.

## How it works

1. Fetches the **ContentDeploymentManifest** from `trapteam-tablet.activision.com`.
2. Keeps only manifest lines with asset URLs on that host.
3. Applies the language rules above.
4. Streams each missing file to disk with a progress percentage.

Manifest URL:

`http://trapteam-tablet.activision.com/Tablet2014/andb/ContentDeploymentManifest.xml.D4C088857665CFB8E70CD26EFAC483D7`

## Notes

- **Resume-friendly:** existing files are skipped; re-run to fill gaps.
- **CDN:** needs `trapteam-tablet.activision.com` to be reachable; endpoints may be offline over time.
- **Legal:** game assets belong to Activision. Use only for allowed preservation, modding, or research.

## Project layout

```
.
├── downloadfiles.py
├── requirements.txt
└── README.md
```

## License

No license is specified for this script. Game assets remain subject to Activision’s terms.

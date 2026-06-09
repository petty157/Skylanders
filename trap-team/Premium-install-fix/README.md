# Skylanders Trap Team — Premium Install Spam Fix

Fixes the **Premium Install notification spam glitch** in Skylanders Trap Team on Android, where the prompt repeatedly appears whenever a Skylander is placed on or removed from the portal.

---

## The Glitch

The game compares your device's free storage against a threshold value (`minFreeSpaceGameFull`) stored in `alchemy.xml`. When your free space exceeds that threshold — which happens once you have more than ~4 GB free — the game incorrectly triggers the Premium Install prompt on every portal interaction.

The fix is to update that threshold to a value above your current free storage so the condition is never met.

---

## What the Script Does

1. Scans all known Android storage paths for the game's `alchemy.xml`
2. Reads the actual free storage of the filesystem where the file lives
3. Sets `minFreeSpaceGameFull` to your current free space + 1 GB, editing the file directly
4. If the file is found in multiple locations (external SD card, secondary user profile, leftover install), it warns you and lets you choose which to patch or patch all at once

---

## Requirements

- [Termux](https://f-droid.org/packages/com.termux/) — free terminal emulator for Android
- Storage permission granted to Termux — run `termux-setup-storage` once if you haven't already
- No root required

---

## Usage

Download `fix_skylanders_glitch.sh`, then in Termux:

```sh
sh fix_skylanders_glitch.sh
```

That's it. You can run it from any directory — it will find the game file automatically.

---

## Re-running

The patched value is tied to your free storage at the time you ran the script. If you later **free up more than 1 GB** of storage (delete large files, clear app data, etc.), your free space could exceed the threshold again and the glitch may return. Just re-run the script to recalculate.

If `alchemy.xml` gets deleted or reset by the game, just run the script again.

---

## Tested Paths

The script checks the following locations automatically:

```
/sdcard
/storage/emulated/0
/storage/emulated/1
/storage/self/primary
/mnt/sdcard
/mnt/user/0/primary
/data/media/0
/storage/<UUID>   (external SD cards, auto-detected)
```

---

## Troubleshooting

**"Cannot write to file — permission denied"**
Run `termux-setup-storage` in Termux and grant storage access when prompted, then try again.

**"Game file not found in any known storage location"**
Make sure Skylanders Trap Team is installed and has been launched at least once. If you have the `alchemy.xml` file manually, place it in the same folder as the script and re-run — it will offer to patch that copy instead.

**The glitch came back**
Your free storage increased past the patched threshold. Re-run the script.

---

## Platform

Tested on Android via Termux. Also runs on Linux and macOS.

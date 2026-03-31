# What this script does
1. Scans public/ recursively
2. Collects all .jpg/.jpeg/.png file paths
3. Converts them into web paths (e.g. /avatars/Yogesh.jpeg)
4. Searches inside src/
5. Replaces only those exact paths → .avif

# How to run
```bash
python replace_images.py
```

## Why this is correct (and your earlier approach was risky)
✅ Safe:
- Only replaces images that actually exist
- Preserves folder structure
- Doesn’t touch random .png strings

## Recommended workflow (don’t skip)
1. Run the image conversion script
2. Run this Python script
3. Run:
```bash
git diff
```
4. Verify changes before commit

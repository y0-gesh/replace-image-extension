# AVIF Migration Tool

A simple and safe Python script to migrate images to `.avif` format by:

- Deleting old image files (`.jpg`, `.jpeg`, `.png`, `.webp`, `.gif`) with the same base name
- Moving the new `.avif` versions into the `public/attachments` directory

Perfect for Next.js, Vite, or any project using a `public/` folder for static assets.

---

## Features

- Automatically detects and deletes all old versions of an image
- Moves new `.avif` files to the correct location in `public/attachments`
- Case-insensitive matching for reliable file handling
- Safe and verbose logging with clear status messages
- Preserves folder structure (ready for subfolder support)

---

## Project Structure
```text
project-root/
├── public/
│   └── attachments/             # Target folder for attachments
├── new_avif/                    # Put your new .avif files here
├── migrate_avif_files.py              # Main script
└── README.md
```

## How to Use

### 1. Setup

1. Place the script (`migrate_avif_files.py`) in your project root.
2. Create a folder named `new_avif` in the project root.
3. Copy all your new `.avif` files into the `new_avif` folder.

### 2. Run the Script

```bash
python migrate_avif_files.py
3. What Happens
For each .avif file:

All old files with the same name (e.g., Blog-9.jpg, blog-9.png, BLOG-9.jpeg) are deleted from public/attachments
The new .avif file is moved to public/attachments/


Configuration
You can customize these variables at the top of migrate_avif_files.py:
PythonPUBLIC_DIR = os.path.join(PROJECT_ROOT, "public", "attachments")
NEW_AVIF_DIR = os.path.join(PROJECT_ROOT, "new_avif")   # Change if needed
OLD_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp", ".gif")

Safety Notes

The script permanently deletes old image files.
Always run it after taking a backup of your public/attachments folder (recommended for the first time).
It only deletes files with the exact same base name (ignoring extension).

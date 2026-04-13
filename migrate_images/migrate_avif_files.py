import os
import shutil
from pathlib import Path

# ========================= CONFIGURATION =========================
PROJECT_ROOT = os.getcwd()

PUBLIC_DIR = os.path.join(PROJECT_ROOT, "public", "attachments")
NEW_AVIF_DIR = os.path.join(PROJECT_ROOT, "new_avif")   # ← Change this if your new files are elsewhere

# Old extensions to delete
OLD_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp", ".gif")

# ================================================================

def get_base_name(filename):
    """Get filename without extension (case insensitive for matching)"""
    return os.path.splitext(filename)[0].lower()


def find_and_delete_old_files(base_name, public_dir):
    """Delete all old versions of the image in public directory"""
    deleted = []
    base_lower = base_name.lower()
    
    for root, _, files in os.walk(public_dir):
        for file in files:
            file_base = get_base_name(file)
            if file_base == base_lower and file.lower().endswith(OLD_EXTENSIONS):
                old_file_path = os.path.join(root, file)
                try:
                    os.remove(old_file_path)
                    deleted.append(file)
                    print(f"🗑️  Deleted: {file}")
                except Exception as e:
                    print(f"Error deleting {file}: {e}")
    return deleted


def main():
    print("AVIF Migration Tool")
    print(f"Public Images Folder : {PUBLIC_DIR}")
    print(f"New AVIF Source      : {NEW_AVIF_DIR}\n")

    if not os.path.exists(NEW_AVIF_DIR):
        print(f"Error: New AVIF folder not found at:\n{NEW_AVIF_DIR}")
        print("Please create the folder and put your new .avif files there.")
        return

    avif_files = [f for f in os.listdir(NEW_AVIF_DIR) if f.lower().endswith(".avif")]

    if not avif_files:
        print("No .avif files found in the new_avif folder.")
        return

    print(f"Found {len(avif_files)} new .avif files.\n")
    
    moved_count = 0

    for avif_file in avif_files:
        base_name = get_base_name(avif_file)
        source_path = os.path.join(NEW_AVIF_DIR, avif_file)
        
        print(f"Processing: {avif_file}")

        # Step 1: Delete old files with same base name
        find_and_delete_old_files(base_name, PUBLIC_DIR)

        # Step 2: Determine destination path (preserving subfolders if any)
        # Currently assuming flat structure. Modify if you have subfolders.
        dest_path = os.path.join(PUBLIC_DIR, avif_file)

        # Step 3: Move the new .avif file
        try:
            shutil.move(source_path, dest_path)
            print(f"Moved: {avif_file} → public/images/")
            moved_count += 1
        except Exception as e:
            print(f"Error moving {avif_file}: {e}")

    print("\n" + "="*60)
    print(f"🎉 Process completed!")
    print(f"   • Total .avif files processed : {len(avif_files)}")
    print(f"   • Successfully moved          : {moved_count}")
    print("="*60)


if __name__ == "__main__":
    main()
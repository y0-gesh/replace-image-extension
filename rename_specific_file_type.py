import os
import re

PROJECT_ROOT = os.getcwd()
PUBLIC_DIR = os.path.join(PROJECT_ROOT, "public/images")
SRC_DIR = os.path.join(PROJECT_ROOT, "src")

# File extensions to look for in source code
OLD_EXTENSIONS = (".jpg", ".jpeg", ".png")
CODE_EXTENSIONS = (".js", ".ts", ".jsx", ".tsx", ".md")

def get_avif_images():
    """Get list of web paths for all .avif images in public"""
    images = []

    for root, _, files in os.walk(PUBLIC_DIR):
        for file in files:
            if file.lower().endswith(".avif"):
                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, PUBLIC_DIR)
                web_path = "/" + relative_path.replace("\\", "/")
                
                # Store both the base name (without extension) and full web path
                base_name = os.path.splitext(file)[0]  # e.g., "Blog-9"
                images.append({
                    "web_path": web_path,           # /Blog-9.avif
                    "base_name": base_name.lower()  # for matching
                })

    return images


def replace_in_file(file_path, avif_images):
    """Replace old image extensions with .avif"""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    original_content = content
    updated = False

    for img in avif_images:
        base = img["base_name"]
        avif_path = img["web_path"]

        # Create regex to match any old extension for this base name
        # Example: Blog-9.png, Blog-9.jpg, Blog-9.jpeg, blog-9.PNG, etc.
        pattern = re.compile(
            rf'({re.escape(base)})\.(jpg|jpeg|png)',
            re.IGNORECASE
        )

        # Replace all occurrences
        new_content = pattern.sub(rf'\1.avif', content)

        if new_content != content:
            content = new_content
            updated = True

    if updated:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✓ Updated: {os.path.relpath(file_path, PROJECT_ROOT)}")
        return True
    return False


def process_src_files(avif_images):
    """Process all source files"""
    if not avif_images:
        print("No .avif images found in public/images")
        return

    print(f"Found {len(avif_images)} .avif images. Updating references...\n")

    updated_count = 0
    for root, _, files in os.walk(SRC_DIR):
        for file in files:
            if file.lower().endswith(CODE_EXTENSIONS):
                file_path = os.path.join(root, file)
                if replace_in_file(file_path, avif_images):
                    updated_count += 1

    print(f"\n✅ Done! Updated {updated_count} files.")


def main():
    print("🚀 AVIF Extension Updater")
    print(f"Public images: {PUBLIC_DIR}")
    print(f"Source folder : {SRC_DIR}\n")

    avif_images = get_avif_images()

    if not avif_images:
        print("No .avif files found. Please check the directory.")
        return

    # Show first 10 images for verification
    print("Found AVIF images:")
    for img in sorted(avif_images, key=lambda x: x["web_path"])[:15]:
        print(f"   • {img['web_path']}")
    if len(avif_images) > 15:
        print(f"   ... and {len(avif_images) - 15} more")

    print("\nStarting replacement in .md and .tsx files...")
    process_src_files(avif_images)


if __name__ == "__main__":
    main()

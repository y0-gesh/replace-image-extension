import os

PROJECT_ROOT = os.getcwd()
PUBLIC_DIR = os.path.join(PROJECT_ROOT, "public")
SRC_DIR = os.path.join(PROJECT_ROOT, "src")

# File extensions to consider as assets in public/images
IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".avif", ".webp", ".gif")

# File extensions to search inside src/
CODE_EXTENSIONS = (".js", ".ts", ".jsx", ".tsx", ".md", ".html", ".css")

def get_all_public_images():
    """Get list of all images in public/images"""
    images = []
    for root, _, files in os.walk(PUBLIC_DIR):
        for file in files:
            if file.lower().endswith(IMAGE_EXTENSIONS):
                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, PUBLIC_DIR)
                web_path = "/" + relative_path.replace("\\", "/")
                base_name = os.path.splitext(file)[0].lower()   # e.g., "blog-9"
                
                images.append({
                    "web_path": web_path,
                    "base_name": base_name,
                    "full_filename": file
                })
    return images


def is_referenced_in_src(base_name):
    """Check if base_name appears anywhere in src/ files (case-insensitive)"""
    base_lower = base_name.lower()
    
    for root, _, files in os.walk(SRC_DIR):
        for file in files:
            if file.lower().endswith(CODE_EXTENSIONS):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read().lower()
                        if base_lower in content:
                            return True
                except Exception:
                    # Skip files that can't be read
                    continue
    return False


def find_unused_assets():
    """Main function to find and list unused assets"""
    print("🚀 Unused Assets Finder")
    print(f"Public images : {PUBLIC_DIR}")
    print(f"Source folder : {SRC_DIR}\n")

    all_images = get_all_public_images()
    
    if not all_images:
        print("❌ No image files found in public")
        return

    print(f"Found {len(all_images)} image files. Scanning for unused ones...\n")

    unused_assets = []
    
    for img in sorted(all_images, key=lambda x: x["web_path"]):
        if not is_referenced_in_src(img["base_name"]):
            unused_assets.append(img)
            print(f"🗑️  UNUSED → {img['web_path']}")

    print("\n" + "="*60)
    if unused_assets:
        print(f"✅ Summary: Found **{len(unused_assets)} unused assets** in public")
        print("\nUnused Assets List:")
        for img in unused_assets:
            print(f"   • {img['web_path']}")
    else:
        print("🎉 Excellent! No unused assets found. All images are being referenced.")

    print("="*60)


if __name__ == "__main__":
    find_unused_assets()
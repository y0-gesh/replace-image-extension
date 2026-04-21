import os

PROJECT_ROOT = os.getcwd()
PUBLIC_DIR = os.path.join(PROJECT_ROOT, "public")
SRC_DIR = os.path.join(PROJECT_ROOT, "src")

IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".avif", ".webp", ".gif")
CODE_EXTENSIONS = (".js", ".ts", ".jsx", ".tsx", ".md", ".html", ".css")
DRY_RUN = False

# ⚠️ Default = safe mode (no deletion)

def get_all_public_images():
    images = []
    for root, _, files in os.walk(PUBLIC_DIR):
        for file in files:
            if file.lower().endswith(IMAGE_EXTENSIONS):
                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, PUBLIC_DIR)
                web_path = "/" + relative_path.replace("\\", "/")
                base_name = os.path.splitext(file)[0].lower()

                images.append({
                    "web_path": web_path,
                    "base_name": base_name,
                    "full_path": full_path
                })
    return images


def is_referenced_in_src(base_name):
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
                    continue
    return False


def find_unused_assets():
    print("🚀 Unused Assets Finder")
    print(f"Public images : {PUBLIC_DIR}")
    print(f"Source folder : {SRC_DIR}")
    print(f"Mode          : {'DRY RUN' if DRY_RUN else 'DELETE'}\n")

    all_images = get_all_public_images()

    if not all_images:
        print("❌ No image files found in public")
        return

    unused_assets = []

    for img in sorted(all_images, key=lambda x: x["web_path"]):
        if not is_referenced_in_src(img["base_name"]):
            unused_assets.append(img)
            print(f"🗑️ UNUSED → {img['web_path']}")

    print("\n" + "=" * 60)

    if not unused_assets:
        print("🎉 No unused assets found.")
        print("=" * 60)
        return

    print(f"Found {len(unused_assets)} unused assets.\n")

    # 🔒 Dry run mode (safe)
    if DRY_RUN:
        print("Dry run enabled → No files deleted.")
        print("=" * 60)
        return

    # ⚠️ Confirmation before delete
    confirm = input("Type 'delete' to permanently remove these files: ")

    if confirm != "delete":
        print("Aborted. No files deleted.")
        return

    # 🧹 Delete files
    deleted = 0
    for img in unused_assets:
        try:
            os.remove(img["full_path"])
            print(f"Deleted → {img['web_path']}")
            deleted += 1
        except Exception as e:
            print(f"Error deleting {img['web_path']}: {e}")

    print("\n" + "=" * 60)
    print(f"Deleted {deleted} files.")
    print("=" * 60)


if __name__ == "__main__":
    find_unused_assets()
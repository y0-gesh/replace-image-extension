import os
import re

PROJECT_ROOT = os.getcwd()
PUBLIC_DIR = os.path.join(PROJECT_ROOT, "public")
SRC_DIR = os.path.join(PROJECT_ROOT, "src")

VALID_EXTENSIONS = (".jpg", ".jpeg", ".png")
CODE_EXTENSIONS = (".js", ".ts", ".jsx", ".tsx")


def get_public_images():
    images = []

    for root, _, files in os.walk(PUBLIC_DIR):
        for file in files:
            if file.lower().endswith(VALID_EXTENSIONS):
                full_path = os.path.join(root, file)

                # Convert to web path (relative to public/)
                relative_path = os.path.relpath(full_path, PUBLIC_DIR)
                web_path = "/" + relative_path.replace("\\", "/")

                images.append(web_path)

    return images


def replace_in_file(file_path, replacements):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    original_content = content

    for img_path in replacements:
        avif_path = re.sub(r"\.(jpg|jpeg|png)$", ".avif", img_path, flags=re.IGNORECASE)

        # Replace only exact matches
        content = content.replace(img_path, avif_path)

    if content != original_content:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated: {file_path}")


def process_src_files(images):
    for root, _, files in os.walk(SRC_DIR):
        for file in files:
            if file.endswith(CODE_EXTENSIONS):
                file_path = os.path.join(root, file)
                replace_in_file(file_path, images)


def main():
    print("Scanning public directory...")
    images = get_public_images()

    print(f"Found {len(images)} images to process")

    print("Updating source files...")
    process_src_files(images)

    print("Done.")


if __name__ == "__main__":
    main()

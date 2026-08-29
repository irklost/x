from pathlib import Path
from PIL import Image, ImageOps
import piexif
import piexif.helper
from datetime import datetime, timezone

current_year = datetime.now(timezone.utc).year

TARGET_SIZES = {
        "4_5": (1080, 1350),
        "16_9": (1920, 1080),
        "1_1": (1080, 1080),
        }

MIN_BORDER = 40  # Minimum border thickness (in pixels) on all four sides
BORDER_COLOR = "white"  # Can be "white", "black", or hex string like "#f4f4f4"
JPEG_QUALITY = 90  # Output JPEG quality (1-100)

CUSTOM_EXIF = {
        "Artist": "Nemo / @irklost",
        "Copyright": f"Copyright {current_year} Nemo. All Rights Reserved.",
        "Description": "Photograph by Nemo (irklost)",
        "Instagram": "https://www.instagram.com/irklost/",
        "YouTube": "https://www.youtube.com/@irklost",
        "Venmo": "https://venmo.com/u/irklost",
        "Cashapp": "https://cash.app/$irklost",
        "Links": "https://linktr.ee/irklost",
        }


def generate_exif_bytes(metadata_dict: dict) -> bytes:
    """Builds a binary EXIF byte payload containing custom tags."""
    # Initialize empty EXIF structure
    exif_dict = {
            "0th": {},
            "Exif": {},
            "GPS": {},
            "1st": {},
            "thumbnail": None,
            }

    # 0th IFD mapping
    if "Artist" in metadata_dict:
        exif_dict["0th"][piexif.ImageIFD.Artist] = metadata_dict["Artist"]
    if "Copyright" in metadata_dict:
        exif_dict["0th"][piexif.ImageIFD.Copyright] = metadata_dict["Copyright"]
    if "ImageDescription" in metadata_dict:
        exif_dict["0th"][piexif.ImageIFD.ImageDescription] = metadata_dict[
                "ImageDescription"
                ]
    if "Make" in metadata_dict:
        exif_dict["0th"][piexif.ImageIFD.Make] = metadata_dict["Make"]
    if "Model" in metadata_dict:
        exif_dict["0th"][piexif.ImageIFD.Model] = metadata_dict["Model"]
    if "Software" in metadata_dict:
        exif_dict["0th"][piexif.ImageIFD.Software] = metadata_dict["Software"]

    # Exif IFD mapping
    if "UserComment" in metadata_dict:
        # Piexif expects encoded byte string for UserComment
        exif_dict["Exif"][piexif.ExifIFD.UserComment] = piexif.helper.UserComment.dump(
                metadata_dict["UserComment"], encoding="unicode"
                )

    return piexif.dump(exif_dict)



def pad_and_resize(
        img: Image.Image, target_size: tuple[int, int], border: int, fill_color: str
        ) -> Image.Image:
    target_w, target_h = target_size

    # 1. Calculate available canvas space inside the border
    inner_w = target_w - (border * 2)
    inner_h = target_h - (border * 2)

    # 2. Resize image maintaining original aspect ratio to fit inside inner canvas
    img_copy = img.copy()
    img_copy.thumbnail((inner_w, inner_h), Image.Resampling.LANCZOS)

    # 3. Create canvas and paste the resized image centered
    canvas = Image.new("RGB", (target_w, target_h), fill_color)
    paste_x = (target_w - img_copy.width) // 2
    paste_y = (target_h - img_copy.height) // 2
    canvas.paste(img_copy, (paste_x, paste_y))

    return canvas


def main():
    img_dir = Path("imgs")
    current_dir = Path.cwd() / img_dir
    image_extensions = {".jpg", ".jpeg", ".JPG", ".JPEG"}

    # Find all JPEGs in current directory
    images = [
            f
            for f in current_dir.iterdir()
            if f.is_file() and f.suffix in image_extensions
            ]

    if not images:
        print("No JPEG images found in the current directory.")
        return

    # Create target directories
    for folder_name in TARGET_SIZES:
        (current_dir / folder_name).mkdir(exist_ok=True)

    # Generate custom EXIF payload once
    custom_exif_bytes = generate_exif_bytes(CUSTOM_EXIF)

    # Process all images
    for img_path in images:
        print(f"Processing: {img_path.name}")
        with Image.open(img_path) as img:
            # Correct orientation from EXIF tags (e.g. phone photos)
            img = ImageOps.exif_transpose(img)
            if img.mode != "RGB":
                img = img.convert("RGB")

            for folder_name, size in TARGET_SIZES.items():
                result_img = pad_and_resize(
                        img, size, MIN_BORDER, BORDER_COLOR
                        )
                output_path = current_dir / folder_name / img_path.name
                result_img.save(
                        output_path, "JPEG", quality=JPEG_QUALITY, optimize=True, exif=custom_exif_bytes,
                        )

    print("\nDone! Images saved to '4_5/', '16_9/', and '1_1/' folders.")


if __name__ == "__main__":
    main()


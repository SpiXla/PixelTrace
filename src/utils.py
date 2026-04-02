from pathlib import Path

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff", ".webp"}

def validate_source_image(image_path: str) -> None:
    source = Path(image_path)

    if not source.exists():
        raise SystemExit(f"Error: image file does not exist: {image_path}")

    if not source.is_file():
        raise SystemExit(f"Error: image path is not a file: {image_path}")

    if source.suffix.lower() not in ALLOWED_EXTENSIONS:
        raise SystemExit(
            "Error: unsupported image format. Supported formats: "
            + ", ".join(sorted(ALLOWED_EXTENSIONS))
        )


def validate_output_path(output_path: str) -> None:
    destination = Path(output_path)

    if destination.name.strip() == "":
        raise SystemExit("Error: output file name cannot be empty")

    if destination.exists() and destination.is_dir():
        raise SystemExit(f"Error: output path is a directory: {output_path}")

    parent = destination.parent
    if str(parent) != "." and not parent.exists():
        raise SystemExit(f"Error: output directory does not exist: {parent}")

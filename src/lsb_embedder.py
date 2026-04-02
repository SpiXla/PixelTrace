from pathlib import Path

from PIL import Image

TEXT_END_MARKER = "\0"

def embed_lsb_data(source_path: str, output_path: str, message: str) -> str:
    payload = (message + TEXT_END_MARKER).encode("utf-8")
    payload_bits = "".join(f"{byte:08b}" for byte in payload)

    with Image.open(source_path) as image:
        rgb_image = image.convert("RGB")
        pixels = list(rgb_image.getdata())

    capacity_bits = len(pixels) * 3
    if len(payload_bits) > capacity_bits:
        raise SystemExit(
            f"Error: message is too large for this image. Capacity: {capacity_bits // 8} bytes."
        )

    updated_pixels = []
    bit_index = 0

    for red, green, blue in pixels:
        channels = [red, green, blue]

        for channel_index in range(3):
            if bit_index >= len(payload_bits):
                break

            bit = int(payload_bits[bit_index])
            channels[channel_index] = (channels[channel_index] & ~1) | bit
            bit_index += 1

        updated_pixels.append(tuple(channels))

    stego_image = Image.new("RGB", rgb_image.size)
    stego_image.putdata(updated_pixels)
    stego_image.save(output_path, format="PNG")
    return output_path


def default_hidden_output_path(source_path: str) -> str:
    source = Path(source_path)
    return str(Path("outputs") / f"{source.stem}_hidden.png")

from pathlib import Path

from PIL import Image

from src.steganography_extractor import (
    KEY_END,
    KEY_START,
    NO_HIDDEN_DATA_MESSAGE,
    TEXT_END_MARKER,
    extract_hidden_data,
)


def create_png(path: Path, size: tuple[int, int] = (20, 20)) -> None:
    image = Image.new("RGB", size, color=(255, 255, 255))
    image.save(path, format="PNG")


def embed_lsb_message(path: Path, message: str) -> None:
    payload = (message + TEXT_END_MARKER).encode("utf-8")
    payload_bits = "".join(f"{byte:08b}" for byte in payload)

    with Image.open(path) as image:
        rgb_image = image.convert("RGB")
        pixels = list(rgb_image.getdata())

    if len(payload_bits) > len(pixels) * 3:
        raise AssertionError("Test image is too small for the hidden payload")

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
    stego_image.save(path, format="PNG")


def test_extracts_plain_lsb_text(tmp_path: Path) -> None:
    image_path = tmp_path / "plain_lsb.png"
    create_png(image_path)
    embed_lsb_message(image_path, "hello from lsb")

    result = extract_hidden_data(str(image_path))

    assert result == "hello from lsb"


def test_extracts_pgp_block_from_lsb_payload(tmp_path: Path) -> None:
    image_path = tmp_path / "pgp_lsb.png"
    create_png(image_path, size=(40, 40))
    key_block = f"{KEY_START}\nabc123\n{KEY_END}"
    embed_lsb_message(image_path, key_block)

    result = extract_hidden_data(str(image_path))

    assert result == key_block


def test_returns_message_when_no_hidden_data_exists(tmp_path: Path) -> None:
    image_path = tmp_path / "clean.png"
    create_png(image_path)

    result = extract_hidden_data(str(image_path))

    assert result == NO_HIDDEN_DATA_MESSAGE

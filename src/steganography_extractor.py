from PIL import Image


KEY_START = "-----BEGIN PGP PUBLIC KEY BLOCK-----"
KEY_END = "-----END PGP PUBLIC KEY BLOCK-----"
TEXT_END_MARKER = "\0"
NO_HIDDEN_DATA_MESSAGE = "No hidden data found in the image."


def extract_hidden_data(image_path: str) -> str:
    direct_key = extract_embedded_key_block(image_path)
    if direct_key:
        return direct_key

    lsb_payload = extract_lsb_data(image_path)
    if not lsb_payload or not looks_like_text(lsb_payload):
        return NO_HIDDEN_DATA_MESSAGE

    start_index = lsb_payload.find(KEY_START)
    if start_index == -1:
        return lsb_payload

    end_index = lsb_payload.find(KEY_END, start_index)
    if end_index == -1:
        return lsb_payload[start_index:]

    end_index += len(KEY_END)
    return lsb_payload[start_index:end_index]


def extract_embedded_key_block(image_path: str) -> str:
    with open(image_path, "rb") as f:
        data = f.read().decode(errors="ignore")

    start_index = data.find(KEY_START)
    if start_index == -1:
        return ""

    end_index = data.find(KEY_END, start_index)
    if end_index == -1:
        return ""

    end_index += len(KEY_END)
    return data[start_index:end_index]


def extract_lsb_data(image_path: str) -> str:
    with Image.open(image_path) as image:
        rgb_image = image.convert("RGB")
        bits = []

        for red, green, blue in rgb_image.getdata():
            bits.append(str(red & 1))
            bits.append(str(green & 1))
            bits.append(str(blue & 1))

    characters = []
    for index in range(0, len(bits), 8):
        byte_bits = bits[index:index + 8]
        if len(byte_bits) < 8:
            break

        value = int("".join(byte_bits), 2)
        if value == 0:
            break

        characters.append(chr(value))

    payload = "".join(characters).strip()
    if not payload:
        return ""

    marker_index = payload.find(TEXT_END_MARKER)
    if marker_index != -1:
        return payload[:marker_index]

    return payload


def looks_like_text(value: str) -> bool:
    if not value:
        return False

    printable_count = sum(1 for char in value if char.isprintable() or char in "\n\r\t")
    printable_ratio = printable_count / len(value)

    alnum_count = sum(1 for char in value if char.isalnum())
    alnum_ratio = alnum_count / len(value)

    return printable_ratio >= 0.95 and alnum_ratio >= 0.30

# PixelTrace

PixelTrace is a small command-line tool for inspecting images. It can:

- extract image metadata such as GPS, device, software, and capture date
- detect hidden text or PGP public key blocks
- hide a message inside an image using least significant bit (LSB) steganography

## Features

- `-m` metadata mode
- `-s` steganography extraction mode
- `-h` / `--hide` steganography embedding mode
- optional `-o` output file support

## Requirements

- Python 3.10+
- dependencies from [`requirements.txt`](/Users/mac/Desktop/PixelTrace/requirements.txt)

## Installation

```bash
python3 -m pip install -r requirements.txt
```

## Usage

Run the CLI with:

```bash
python3 main.py [option] <image_path> [message] [-o output_path]
```

### Show Help

```bash
python3 main.py --help
```

### Extract Metadata

```bash
python3 main.py -m sample_images/image-example-full.jpeg
```

Example output:

```text
Latitude: Not found
Longitude: Not found
Resolution: 1920x1080
Device: Not found
Software: Not found
Date: Not found
```

Save metadata to a file:

```bash
python3 main.py -m sample_images/image-example-full.jpeg -o outputs/metadata.txt
```

### Extract Hidden Data

```bash
python3 main.py -s sample_images/image-example-full.jpeg
```

This mode checks for:

- directly embedded text containing a PGP public key block
- text reconstructed from RGB least significant bits

If nothing meaningful is found, the tool returns:

```text
No hidden data found in the image.
```

Save extracted hidden data to a file:

```bash
python3 main.py -s sample_images/image-example-full.jpeg -o outputs/hidden.txt
```

### Hide a Message in an Image

Hide a message with LSB steganography:

```bash
python3 main.py -h sample_images/image-example1.jpeg "hello from PixelTrace"
```

By default, this saves a new PNG in `outputs/`:

```text
outputs/image-example1_hidden.png
```

You can choose the output file yourself:

```bash
python3 main.py -h sample_images/image-example1.jpeg "hello from PixelTrace" -o outputs/custom_hidden.png
```

Then test extraction:

```bash
python3 main.py -s outputs/custom_hidden.png
```

## How Steganography Works Here

### Extraction

PixelTrace first tries to find a visible embedded PGP public key block in the file contents. If that fails, it reads the least significant bit from each RGB channel and reconstructs text from those bits.

### Embedding

Hide mode stores the message in the RGB LSBs of the output image and appends a null terminator so extraction knows where the message ends.

## Important Notes

- LSB embedding is most reliable when the output image is saved as `PNG`
- basic LSB techniques are not reliable with `JPEG` output because compression changes pixel values
- the hide mode always saves a `PNG`
- extraction includes a simple text-quality check to avoid displaying random garbage from images with no hidden payload

## Project Structure

```text
.
├── main.py
├── requirements.txt
├── sample_images/
├── outputs/
├── src/
│   ├── analyzer.py
│   ├── cli.py
│   ├── lsb_embedder.py
│   ├── metadata_extractor.py
│   ├── report_writer.py
│   ├── steganography_extractor.py
│   └── utils.py
└── tests/
    ├── test_metadata.py
    └── test_steganography.py
```

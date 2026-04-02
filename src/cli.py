import sys
from typing import Sequence

from src.analyzer import (
    handle_combined_analysis,
    handle_metadata_analysis,
    handle_steganography_analysis,
    handle_steganography_hide,
)
from src.utils import validate_output_path, validate_source_image


HELP_TEXT = """Welcome to Image Inspector

OPTIONS:
    -m  Metadata          Extract metadata from the image (e.g., geolocation, device info)
    -s  Steganography     Detect and extract hidden data from the image using steganography techniques
        You can combine -m and -s in one command
    -h, --hide            Hide a message in the image using LSB steganography
    -o  "FileName"        Specify the file name to save output
    --help                Display this help message
"""


def print_help() -> None:
    print(HELP_TEXT)


def default_args() -> dict:
    return {
        "modes": set(),
        "output": None,
        "image_path": None,
        "message": None,
    }


def parse_args(args: Sequence[str] | None = None) -> dict:
    arguments = list(sys.argv[1:] if args is None else args)

    if not arguments:
        raise SystemExit("Error: no arguments provided. Use --help for usage.")

    if len(arguments) == 1 and arguments[0] == "--help":
        print_help()
        raise SystemExit(0)

    parsed = default_args()
    index = 0

    while index < len(arguments):
        argument = arguments[index]

        if argument == "--help":
            raise SystemExit("Error: --help must be used alone")

        if argument in ("-m", "-s", "-h", "--hide"):
            parsed = parse_mode_argument(parsed, argument)
            index += 1
            continue

        if argument == "-o":
            parsed, index = parse_output_argument(parsed, arguments, index)
            continue

        if argument.startswith("-"):
            raise SystemExit(f"Error: unknown option '{argument}'")

        parsed = parse_image_argument(parsed, argument)
        index += 1

    validate_args(parsed)
    return parsed


def parse_mode_argument(parsed: dict, argument: str) -> dict:
    if argument == "-m":
        selected_mode = "metadata"
    elif argument == "-s":
        selected_mode = "steganography"
    else:
        selected_mode = "hide"

    if selected_mode in parsed["modes"]:
        raise SystemExit(f"Error: option '{argument}' cannot be used more than once")

    if selected_mode == "hide" and parsed["modes"]:
        raise SystemExit("Error: -h cannot be combined with -m or -s")

    if selected_mode in {"metadata", "steganography"} and "hide" in parsed["modes"]:
        raise SystemExit("Error: -h cannot be combined with -m or -s")

    parsed["modes"].add(selected_mode)
    return parsed


def parse_output_argument(parsed: dict, arguments: list[str], index: int) -> tuple[dict, int]:
    if parsed["output"] is not None:
        raise SystemExit("Error: -o cannot be used more than once")

    if index + 1 >= len(arguments):
        raise SystemExit("Error: missing file name after -o")

    output_name = arguments[index + 1].strip()
    if not output_name:
        raise SystemExit("Error: output file name cannot be empty")

    if output_name.startswith("-"):
        raise SystemExit("Error: invalid output file name")

    parsed["output"] = output_name
    return parsed, index + 2


def parse_image_argument(parsed: dict, argument: str) -> dict:
    if parsed["image_path"] is not None:
        if "hide" in parsed["modes"] and parsed["message"] is None:
            parsed["message"] = argument
            return parsed

        raise SystemExit("Error: too many positional arguments provided")

    if not argument.strip():
        raise SystemExit("Error: image file path cannot be empty")

    parsed["image_path"] = argument
    return parsed


def validate_args(parsed: dict) -> None:
    if not parsed["modes"]:
        raise SystemExit("Error: choose -m, -s, or -h")

    if parsed["image_path"] is None:
        raise SystemExit("Error: missing image file path")

    validate_source_image(parsed["image_path"])

    if "hide" in parsed["modes"] and parsed["message"] is None:
        raise SystemExit("Error: missing message to hide in the image")

    if parsed["output"] is not None:
        validate_output_path(parsed["output"])


def dispatch(parsed: dict) -> str:
    if parsed["modes"] == {"metadata"}:
        return handle_metadata_analysis(parsed["image_path"], parsed["output"])

    if parsed["modes"] == {"steganography"}:
        return handle_steganography_analysis(parsed["image_path"], parsed["output"])

    if parsed["modes"] == {"metadata", "steganography"}:
        return handle_combined_analysis(parsed["image_path"], parsed["output"])

    return handle_steganography_hide(parsed["image_path"], parsed["message"], parsed["output"])


def main(args: Sequence[str] | None = None) -> int:
    parsed = parse_args(args)
    result = dispatch(parsed)
    if result:
        print(result)
    return 0

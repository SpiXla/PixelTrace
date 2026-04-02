from src.metadata_extractor import extract_metadata
from src.lsb_embedder import default_hidden_output_path, embed_lsb_data
from src.report_writer import save_report
from src.steganography_extractor import extract_hidden_data


def handle_metadata_analysis(image_path: str, output_path: str | None = None) -> str:
    result = extract_metadata(image_path)
    return finalize_result(result, output_path)


def handle_steganography_analysis(image_path: str, output_path: str | None = None) -> str:
    result = extract_hidden_data(image_path)
    return finalize_result(result, output_path)


def handle_combined_analysis(image_path: str, output_path: str | None = None) -> str:
    metadata_result = extract_metadata(image_path)
    steganography_result = extract_hidden_data(image_path)
    combined_result = (
        "Metadata Analysis\n"
        f"{metadata_result}\n\n"
        "Steganography Analysis\n"
        f"{steganography_result}"
    )
    return finalize_result(combined_result, output_path)


def handle_steganography_hide(
    image_path: str,
    message: str,
    output_path: str | None = None,
) -> str:
    destination = output_path if output_path is not None else default_hidden_output_path(image_path)
    embed_lsb_data(image_path, destination, message)
    return f"Hidden data saved in {destination}"


def finalize_result(result: str, output_path: str | None = None) -> str:
    if output_path is None:
        return result

    save_report(output_path, result)
    return f"{result}\nData saved in {output_path}"

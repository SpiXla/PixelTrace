from src.metadata_extractor import extract_metadata
from src.report_writer import save_report
from src.steganography_extractor import extract_hidden_data


def handle_metadata_analysis(image_path: str, output_path: str | None = None) -> str:
    result = extract_metadata(image_path)
    return finalize_result(result, output_path)


def handle_steganography_analysis(image_path: str, output_path: str | None = None) -> str:
    result = extract_hidden_data(image_path)
    return finalize_result(result, output_path)


def finalize_result(result: str, output_path: str | None = None) -> str:
    if output_path is None:
        return result

    save_report(output_path, result)
    return f"{result}\nData saved in {output_path}"

from pathlib import Path


def save_report(output_path: str, content: str) -> None:
    destination = resolve_output_path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)

    with open(destination, "w", encoding="utf-8") as output_file:
        output_file.write(content)


def resolve_output_path(output_path: str) -> Path:
    destination = Path(output_path)
    if destination.parent == Path("."):
        return Path("outputs") / destination

    return destination

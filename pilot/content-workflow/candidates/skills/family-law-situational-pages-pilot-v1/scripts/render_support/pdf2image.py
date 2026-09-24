"""Small compatibility adapter for Codex's packaged DOCX renderer.

The packaged renderer imports two pdf2image functions, but Poppler is not
available in this workspace. This local adapter implements only the signatures
that renderer uses, backed by PyMuPDF. It is not a general pdf2image replacement.
"""

from __future__ import annotations

from pathlib import Path

import fitz


def pdfinfo_from_path(pdf_path: str) -> dict[str, object]:
    document = fitz.open(pdf_path)
    try:
        page = document[0]
        rect = page.rect
        return {
            "Pages": document.page_count,
            "Page size": f"{rect.width:g} x {rect.height:g} pts",
        }
    finally:
        document.close()


def convert_from_path(
    pdf_path: str,
    dpi: int = 200,
    fmt: str = "png",
    thread_count: int = 1,
    output_folder: str | None = None,
    paths_only: bool = False,
    output_file: str = "page",
    **_unused: object,
):
    if fmt.lower() != "png":
        raise ValueError("This compatibility adapter supports PNG output only.")
    if not paths_only or output_folder is None:
        raise ValueError("This adapter supports only paths_only=True with output_folder.")
    del thread_count
    output_dir = Path(output_folder)
    output_dir.mkdir(parents=True, exist_ok=True)
    document = fitz.open(pdf_path)
    results: list[str] = []
    try:
        scale = dpi / 72.0
        matrix = fitz.Matrix(scale, scale)
        for index, page in enumerate(document):
            output_path = output_dir / f"{output_file}-local-{index + 1}.png"
            page.get_pixmap(matrix=matrix, alpha=False).save(output_path)
            results.append(str(output_path))
    finally:
        document.close()
    return results
